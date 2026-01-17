# Parser Industry-Hardstyle-Sex
# Copyright 2026 t.me/Dinger_JC



# Основное
from logger import Log
from curl_cffi import requests
from bs4 import BeautifulSoup
import yt_dlp
import ffmpeg
from urllib.parse import urlparse

# Работа с файлами
import re
import os
from pathlib import Path
import json

# Другое
from typing import Any
from datetime import timedelta
import math
import sys
import random
import string
from fractions import Fraction
from pprint import pprint



class App:
    '''Industry-Hardstyle-Sex'''
    def __init__(self):
        '''Основное'''
        # Проверка необходимых файлов
        self.data = 'data.json'
        self.ffmpeg = 'ffmpeg.exe'
        self.ffprobe = 'ffprobe.exe'
        self.CheckRequiredFiles(self.data, self.ffmpeg, self.ffprobe)

        # Обработка данных из файла
        with open(self.data, encoding ='utf-8') as file:
            links = json.load(file)
        self.sites = links['sites']
        self.url = links['videos']['4']
        self.domain: str = urlparse(self.url).netloc
        log.info(f'Ссылка: {self.url}')
        log.info(f'Сайт: {self.domain}')

        # Директория
        self.name_folder: str = 'Saved Videos'
        self.folder: str = Path.home() / 'Desktop' / self.name_folder
        self.folder.mkdir(parents = True, exist_ok = True)

        # Название кэша
        self.symbols: str = string.ascii_letters + string.digits + '_' * 5 + '-' * 5
        self.filename: str = ''.join(random.choice(self.symbols) for _ in range(32))
        self.file: str = f'{self.folder / self.filename}.mp4'

        # Заголовки HTTP-запросов
        self.headers: dict[str, str] = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', # Имитация браузера Chrome (TLS/HTTP2) для обхода защиты
            'referer': f'https://{self.domain}/', # Указывает серверу, с какой страницы пришел запрос
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8', # Языки
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="143", "Chromium";v="143"', # Движок
            'sec-ch-ua-mobile': '?0', # Платформа
            'sec-ch-ua-platform': '"Windows"', # ОС
            'sec-fetch-mode': 'no-cors', # Режим запроса без CORS
            'sec-fetch-site': 'cross-site' # Запрос идет на другой домен
        }

        # Настройки для yt_dlp
        self.yt_dlp_options: dict[str, Any] = {
            'http_headers': self.headers,
            'progress_hooks': [self.ProgressBar], # Отслеживание прогресса загрузки
            'outtmpl': self.file, # Путь сохраняемого файла
            'format': 'bestvideo+bestaudio/best', # Качество видео
            'ffmpeg_location': str(Path(__file__).parent.absolute() / self.ffmpeg), # Путь ffmpeg
            'merge_output_format': 'mp4', # Формат после загрузки
            'socket_timeout': 15, # Время ожидания ответа от сервера (в секундах)
            'sleep_interval': 0, # Минимальная пауза между загрузками (в секундах)
            'max_sleep_interval': 2, # Максимальная случайная пауза между запросами (в секундах)
            'retries': 3, # Количество попыток переподключения при ошибке загрузки файла
            'fragment_retries': 3, # Количество попыток загрузки каждого отдельного фрагмента видео
            'rm_cached_metadata': True, # Очистка метаданных из кэша перед началом загрузки
            'nocheckcertificate': True, # Игнорировать ошибки проверки SSL-сертификатов
            'quiet': True, # Лог
            'verbose': False # Подробный лог
        }

        # Настройки для ffprobe
        self.ffprobe_options: dict[str, Any] = {
            'headers': "".join([f"{k}: {v}\r\n" for k, v in self.headers.items()]), # Заголовки HTTP-запросов
            'analyzeduration': '5000000', # Время на чтение данных (в микросекундах)
            'probesize': '5000000', # Максимальный объем данных для анализа (в микросекундах)
            'rw_timeout': '10000000', # Общее время на операцию (в микросекундах)
            'reconnect_delay_max': '5', # Максимальное время ожидания (в секундах)
            'tls_verify': '0', # Отключает проверку SSL-сертификатов
            'reconnect': '1', # Автоматическое переподключение
            'seekable': '0', # Чтение потока последовательно
            'reconnect_streamed': '1' # Автоматическое переподключение для стримов
        }

    def CheckRequiredFiles(self, data: str, ffmpeg: str, ffprobe: str):
        '''Проверка наличия необходимых файлов'''
        link: str = 'https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45'
        error: bool = False

        if not os.path.exists(ffmpeg):
            log.error(f'Файл "{ffmpeg}" не найден. Скачать его можно здесь: {link}')
            error = True

        if not os.path.exists(ffprobe):
            log.error(f'Файл "{ffprobe}" не найден. Скачайте его здесь: {link}')
            error = True

        if not os.path.exists(data):
            log.error(f'Файл "{data}" не найден')
            error = True

        if error:
            sys.exit(0)

    def FormatUnits(self, value: int, format: str = '') -> str:
        '''Конвертация байтов'''
        factor: dict[str, int] = {
            'KiB': 1024,
            'MiB': 1024 ** 2,
            'GiB': 1024 ** 3
        }

        if value is None or value == 0:
            return 'N/A'

        if value < factor['KiB']:
            return f'{value} B' + format

        if value < factor['MiB']:
            return f'{value / factor['KiB']:.3f} KiB' + format

        if value < factor['GiB']:
            return f'{value / factor['MiB']:.3f} MiB' + format

        return f'{value / factor['GiB']:.3f} GiB' + format

    def ProgressBar(self, data: Any):
        '''Индикатор загрузки'''
        if data['status'] == 'downloading':
            speed: int = data.get('speed')
            volume = data.get('total_bytes') or data.get('total_bytes_estimate')
            downloaded = data.get('downloaded_bytes', 0)
            percent = round(downloaded / volume * 100, 2)

            print(f'\r[СКАЧИВАНИЕ] Прогресс: {percent:.2f}% | Скорость: {self.FormatUnits(speed, '/s')} | Размер: {self.FormatUnits(volume)}', end = '')

        elif data['status'] == 'finished':
            counter = 1
            while True:
                new_name: str = Path(self.folder) / f'{self.site} Video-{counter}.mp4'
                if not new_name.exists():
                    os.rename(self.file, new_name)
                    break
                counter += 1

            log.info(f'Видео успешно скачалось в {self.folder}')

    def CheckLink(self, response: str) -> str:
        '''Проверка ответа страницы'''
        code: int = response.status_code
        errors: dict[str, str] = {
            400: 'некорректный запрос',
            401: 'требуется авторизация',
            403: 'доступ запрещён',
            404: 'страница не найдена',
            408: 'сервер не дождался ответа',
            429: 'слишком много запросы',
            500: 'внутрненняя ошибка сервера',
            502: 'проблема с соединением между серверами',
            503: 'сервер временно перегружен'
        }

        if code in [200, 206]:
            return
        else:
            log.error(f'Ошибка {code}: {errors.get(code, errors.keys())}')
            sys.exit(0)

    def GetResolution(self, width: int, height: int) -> str:
        '''Получение типа разрешения'''
        quality_types: dict[str: [int]] = {
            'LD': [426, 240],
            'SD': [640, 360],
            'HD': [1280, 720],
            'Full HD': [1920, 1080],
            '2K Quad HD': [2560, 1440]
        }

        if [width, height] == quality_types['SD']:
            return f'SD {width}x{height}'

        elif [width, height] == quality_types['HD']:
            return f'HD {width}x{height}'

        elif [width, height] == quality_types['Full HD']:
            return f'Full HD {width}x{height}'

        elif [width, height] == quality_types['2K Quad HD']:
            return f'2K Quad HD {width}x{height}'

        else:
            return f'Другое {width}x{height}'

    def GetInfo(self, url: str, domain: str, sites: dict):
        '''Получение данных с сайта'''
        # Получение ссылки с сайта
        try:
            response = requests.get(url, timeout = 15)
            self.CheckLink(response)

        except requests.exceptions.ConnectionError:
            log.error(f'Не удалось найти сайт {domain}')
            sys.exit(0)

        except requests.exceptions.Timeout:
            log.error(f'Сайт {domain} отвечал слишком долго')
            sys.exit(0)

        page = BeautifulSoup(response.text, 'html.parser')
        self.video_url: str = None

        # Проверка домена
        if domain == list(sites.values())[0]:
            raw_title: str = page.find('title').text
            title: str = re.sub(r'\s*[-–—]\s*Strip2.co\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site: str = 'Strip2'

            links = []
            self.video_url = page.find_all('a', href = True)
            for link in self.video_url:
                if 'vps402.strip2.co.mp4' in link['href']:
                    links.append(link['href'])

            for i, href in enumerate(links):
                find_link: str = str(href)
                if find_link and f'/x{len(links) - 1}/' in find_link:
                    self.video_url: str = find_link

        elif domain == list(sites.values())[1]:
            raw_title: str = page.find('title').text
            title: str = re.sub(r'\s*[-–—]\s*AnalMedia\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site: str = 'AnalMedia'

            video: str = page.find('video')
            self.video_url: str = video.find('source')['src']

        else:
            log.error('Загрузка со сторонних сайтов невозможна. Cкачивание возможно только с сайтов Strip2 и AnalMedia')
            sys.exit(0)

        log.info(f'Название: {title}')
        log.info(f'Прямая ссылка: {self.video_url}')

        # Получение дополнительной информации
        video_info = ffmpeg.probe(self.video_url, **self.ffprobe_options)
        video_stream = next((stream for stream in video_info['streams'] if stream['codec_type'] == 'video'), None)

        width = video_stream.get('width', 0)
        height = video_stream.get('height', 0)
        log.info(f'Разрешение: {self.GetResolution(width, height)}')

        fps = math.ceil(float(Fraction(video_stream.get('avg_frame_rate'))))
        log.info(f'FPS: {fps}')

        duration = video_stream.get('duration')
        if duration is None:
            duration = 'N/A'
        else:
            duration: str = str(timedelta(seconds = float(video_stream.get('duration')))).split('.')[0]
        log.info(f'Длительность: {duration}')

    def GetVideo(self, video_url: str):
        '''Скачивание видео'''
        log.info('Видео начало скачиваться')
        with yt_dlp.YoutubeDL(self.yt_dlp_options) as video:
            video.download([video_url])



if __name__ == '__main__':
    try:
        log = Log(__name__)
        log.info('Запуск')
        app = App()
        app.GetInfo(app.url, app.domain, app.sites)
        app.GetVideo(app.video_url)

    except Exception as error:
        log.error(f'Непредвиденная ошибка: {error}')
