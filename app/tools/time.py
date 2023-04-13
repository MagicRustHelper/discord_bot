ONE_HOUR_SECONDS = 3600


def human_time(seconds: int) -> str:
    text = ''
    hours = int(seconds // ONE_HOUR_SECONDS)
    if hours > 0:
        hours_word = num_to_words(hours, word_forms=('час', 'часа', 'часов'))
        text += f'{hours} {hours_word}'

    minutes = int((seconds - hours * ONE_HOUR_SECONDS) // 60)
    if minutes > 0:
        minutes_word = num_to_words(minutes, word_forms=('минута', 'минуты', 'минут'))
        text += f' {minutes} {minutes_word}'

    if text == '':
        seconds_text = num_to_words(seconds, word_forms=('секунда', 'секунды', 'секунд'))
        return f'{int(seconds)} {seconds_text}'

    return text


def num_to_words(count: int, word_forms: tuple[str, str, str]) -> str:
    if count % 10 == 1 and count % 100 != 11:
        p = 0
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        p = 1
    else:
        p = 2
    return word_forms[p]
