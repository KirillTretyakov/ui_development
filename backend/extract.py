import re


def normalize_text(text: str) -> str:
    """
    Нормализует текст резюме:
    - заменяет неразрывные пробелы;
    - заменяет узкие пробелы;
    - приводит переносы строк к единому виду.
    """

    text = str(text)
    text = text.replace("\xa0", " ")
    text = text.replace("\u202f", " ")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text


def extract_title(text):
    """
    Извлекает профессию / желаемую должность.

    В твоем формате резюме название должности находится
    в первой непустой строке.
    """

    text = normalize_text(text)

    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return None

    return lines[0]


def extract_exp(text):
    """
    Извлекает общий опыт работы из строки вида:

    Опыт работы 2 года 8 месяцев
    Опыт работы — 2 года 8 месяцев
    Опыт работы - 3 года
    Опыт работы 11 месяцев

    Возвращает опыт в годах: например, 2.67.
    """

    text = normalize_text(text).lower()

    pattern = (
        r"опыт\s+работы\s*[—–-]?\s*"
        r"(?:(?P<years>\d+)\s*(?:год|года|лет))?"
        r"\s*"
        r"(?:(?P<months>\d+)\s*(?:месяц|месяца|месяцев))?"
    )

    match = re.search(pattern, text, flags=re.IGNORECASE)

    if not match:
        return None

    years = int(match.group("years")) if match.group("years") else 0
    months = int(match.group("months")) if match.group("months") else 0

    if years == 0 and months == 0:
        return None

    return round(years + months / 12, 2)


def extract_skills(text):
    """
    Извлекает навыки из блока после слова 'Навыки'.

    Логика:
    - ищем отдельную строку 'Навыки';
    - берем текст после нее;
    - останавливаемся на разделе 'Обо мне' или других крупных разделах;
    - удаляем служебные строки с уровнями владения.
    """
    text = normalize_text(text)
    matches = list(
        re.finditer(
            r"^Навыки\s*$",
            text,
            flags=re.IGNORECASE | re.MULTILINE
        )
    )
    if not matches:
        return []
    last_match = matches[-1]
    block = text[last_match.end():].strip()
    stop_pattern = re.compile(
        r"^(Обо мне|Знание языков|Повышение квалификации, курсы|Гражданство, время в пути до работы)\s*$",
        flags=re.IGNORECASE | re.MULTILINE
    )
    stop_match = stop_pattern.search(block)
    if stop_match:
        block = block[:stop_match.start()].strip()
    lines = block.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    skip_lines = {
        "уровни владения навыками",
        "продвинутый уровень",
        "средний уровень",
        "базовый уровень",
        "уровень не указан",
        "опыт вождения",
        "имеется собственный автомобиль",
        "права категории b",
        "водительское удостоверение категории b"
    }

    skills = []

    for line in lines:
        normalized_line = line.lower().strip()

        if normalized_line in skip_lines:
            continue

        skills.append(line)

    return skills