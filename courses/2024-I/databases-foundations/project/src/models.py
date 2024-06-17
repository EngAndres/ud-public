from pydantic import BaseModel


class Country(BaseModel):
    """This class represents the expected data structure for a country"""

    code: int
    name: str


class SubscriberByChannel(BaseModel):
    """This class represents the expected data structure for a subscriber by channel"""

    channel: str
    description: str
    username: str


class VideosCountry(BaseModel):
    """This class represents the expected data structure for a video"""

    name: str
    description: str
    likes: int
    dislikes: int
    user_name: str


class ChannelCountry(BaseModel):
    """This class represents the expected data structure for a channel"""

    name: str
    description: str


class Users(BaseModel):
    """This class represents the expected data structure for a user"""

    name: str
    email: str
    nickname: str
    country: str
    bank: str
    bank_account: str


class MusicalGenre(BaseModel):
    """This class represents the expected data structure for a musical genre"""

    name: str
    description: str
    videos: int


class ReportUgly(BaseModel):
    """This class represents the expected data structure for a report of videos based on comments"""

    name: str
    video_date: str
    video_likes: int
    video_dislikes: int
    comment_content: str
    comment_likes: int
    comment_dislikes: int
    comment_date: str
    comment_user: str
    user_email: str
