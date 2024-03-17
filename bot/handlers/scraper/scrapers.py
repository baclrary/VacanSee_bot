import httpx
from bs4 import BeautifulSoup

from database.crud import assign_vacancy_to_config, create_vacancy

from .utils import fetch_with_retry


class BaseScrapper:
    def __init__(self, config):
        self.config = config
        self.base_url: str = ""
        self.client: httpx.AsyncClient = httpx.AsyncClient(follow_redirects=True)

    async def _fetch_content(self, url: str) -> str:
        print(url)
        response = await fetch_with_retry(self.client, url)
        return response.text

    async def _get_parsed_html(self) -> BeautifulSoup:
        html_content = await self._fetch_content(self.base_url)
        return BeautifulSoup(html_content, "html.parser")

    def _build_url(self) -> str:
        pass


class DouScrapper(BaseScrapper):
    def __init__(self, config):
        super().__init__(config)
        self.base_url = "https://jobs.dou.ua/vacancies/?"
        self.new_vacancies = []

    def _build_url(self):
        exp_ranges = [(0, "0-1"), (1, "1-3"), (3, "3-5"), (5, "5plus")]
        exp_range = next((r for exp, r in reversed(exp_ranges) if self.config.exp_years >= exp), "0-1")
        region_filter = "remote&" if self.config.region.lower() == "remote" else f"city={self.config.region}&"
        self.base_url += f"category={self.config.lang}&exp={exp_range}&{region_filter}"
        if self.config.search_words:
            words = self.config.search_words.replace(" ", "+")
            self.base_url += f"search={words}&descr=1&"

    def _parse_vacancy(self, vacancy):
        date = vacancy.find(class_="date").text.strip()
        title_link = vacancy.find(class_="vt")
        title = title_link.text.strip()
        link = title_link["href"]
        company_name = vacancy.find(class_="company").text.strip()
        location = vacancy.find(class_="cities").text.strip()
        description = vacancy.find(class_="sh-info").text.strip()

        return {
            "url": link,
            "title": title,
            "date": date,
            "location": location,
            "company_name": company_name,
            "description": description,
        }

    async def start(self):
        self._build_url()
        soup = await self._get_parsed_html()
        vacancies_elements = soup.find_all(class_="l-vacancy")

        for vacancy in vacancies_elements:
            vacancy_data = self._parse_vacancy(vacancy)
            created_vacancy_id = await create_vacancy(**vacancy_data)
            result = await assign_vacancy_to_config(created_vacancy_id, self.config.id)
            if result:
                self.new_vacancies.append(vacancy_data)


class DjinniScrapper:
    pass


class RobotaUaScrapper:
    pass
