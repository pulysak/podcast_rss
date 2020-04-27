from django.db import models


class Author(models.Model):
    name = models.CharField('Name', max_length=256)
    email = models.EmailField('Email')

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.name


class Show(models.Model):
    class Type(models.TextChoices):
        EPISODIC = 'episodic', 'Episodic'
        SERIAL = 'serial', 'Serial'

    name = models.CharField('Name', max_length=256)
    slug = models.SlugField('Slug', unique=True)
    long_description = models.TextField('Long description', max_length=4000)
    image = models.URLField('Image')
    language = models.CharField('Language', max_length=256)
    category = models.CharField('Category', max_length=256)
    subcategory = models.CharField('Subcategory', max_length=256, blank=True)
    website = models.URLField('Website link')
    copyright = models.CharField('Copyright', max_length=256)
    type = models.CharField(
        'Type',
        max_length=9,
        choices=Type.choices,
        default=Type.EPISODIC,
    )

    is_released_in_seasons = models.BooleanField('Is released in seasons?', default=False)
    is_include_explicit_language = models.BooleanField('Is include explicit language?', default=False)
    is_blocked = models.BooleanField('Is blocked?', default=False)
    is_complete = models.BooleanField('Is complete?', default=False)

    author = models.ForeignKey(
        Author, verbose_name='author', related_name='shows', on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = 'show'
        verbose_name_plural = 'show'

    def __str__(self):
        return self.name


class Episode(models.Model):
    class EpisodeType(models.TextChoices):
        FULL = 'full', 'Full'
        TRAILER = 'trailer', 'Trailer'
        BONUS = 'bonus', 'Bonus'

    class FileType(models.TextChoices):
        AUDIO_X_M4A = 'audio/x-m4a'
        AUDIO_MPEG = 'audio/mpeg'
        VIDEO_QUICKTIME = 'video/quicktime'
        VIDEO_MP4 = 'video/mp4'
        VIDEO_X_M4V = 'video/x-m4v'
        APPLICATION_PDF = 'application/pdf'

    title = models.CharField('Title', max_length=256)
    notes = models.TextField('Notes')
    episode_number = models.PositiveIntegerField('Episode number', null=True, blank=True)
    season_number = models.PositiveIntegerField('Season number', null=True, blank=True)
    type = models.CharField('Episode type', max_length=8, choices=EpisodeType.choices, default=EpisodeType.FULL)
    is_blocked = models.BooleanField('Is blocked?', default=False)

    file_url = models.URLField('File url')
    file_length = models.IntegerField('File size in bytes')
    file_type = models.CharField('File Type', choices=FileType.choices, max_length=24, default=FileType.AUDIO_MPEG)

    publication_date = models.DateTimeField('Publication date')
    duration = models.IntegerField('Duration in sec', null=True, blank=True)
    link = models.URLField('Episode link', blank=True)
    image = models.URLField('Image', blank=True)
    is_include_explicit_language = models.BooleanField('Is include explicit language?', default=False)

    show = models.ForeignKey(Show, verbose_name='show', related_name='episodes', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'episode'
        verbose_name_plural = 'episodes'

    def __str__(self):
        return self.title
