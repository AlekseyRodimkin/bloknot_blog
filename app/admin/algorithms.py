from collections import Counter
from app.models import Post
from app import db


def get_top_words(top_n=5, batch_size=1000):
    """Функция для получения топ-N самых часто используемых слов во всех постах.

    Args:
        top_n (int): Количество топ слов для возврата. По умолчанию 10.
        batch_size (int): Размер партии для загрузки данных из базы данных. По умолчанию 1000.

    Returns:
        list[tuple[str, int]]: Список кортежей ('слово', количество_использований) в порядке убывания частоты.
    """
    word_counter = Counter()
    offset = 0
    while True:
        posts = db.session.query(Post.body).order_by(Post.id).limit(batch_size).offset(offset).all()
        if not posts:
            break

        for post in posts:
            words = post.body.lower().split()
            word_counter.update(words)

        offset += batch_size

    return word_counter.most_common(top_n)
