"""Data models for Padlet scraping."""

from typing import Optional
from pydantic import BaseModel, Field


class Link(BaseModel):
    """Represents a hyperlink within a post."""

    url: str = Field(description="The URL of the link")
    text: str = Field(description="The display text of the link")

    def __str__(self) -> str:
        return f"[{self.text}]({self.url})"


class Post(BaseModel):
    """Represents a single post within a Padlet section.

    Note: Links are stored inline as Markdown [text](url) format within the body field.
    """

    subject: str = Field(description="The subject/title of the post")
    body: str = Field(description="The body content of the post (with inline Markdown links)")
    section_id: Optional[str] = Field(default=None, description="ID of the parent section")

    def __str__(self) -> str:
        return f"{self.subject}: {self.body[:50]}..." if len(self.body) > 50 else f"{self.subject}: {self.body}"


class Section(BaseModel):
    """Represents a section/column in a Padlet board."""

    title: str = Field(description="The title of the section")
    section_id: Optional[str] = Field(default=None, description="Unique identifier for the section")
    posts: list[Post] = Field(default_factory=list, description="Posts within this section")

    def __str__(self) -> str:
        return f"Section '{self.title}' with {len(self.posts)} post(s)"


class Padlet(BaseModel):
    """Represents a complete Padlet board with all its sections and posts."""

    url: str = Field(description="The URL of the Padlet board")
    title: Optional[str] = Field(default=None, description="The title of the Padlet board")
    sections: list[Section] = Field(default_factory=list, description="Sections within the Padlet")

    @property
    def total_posts(self) -> int:
        """Calculate total number of posts across all sections."""
        return sum(len(section.posts) for section in self.sections)

    def __str__(self) -> str:
        return f"Padlet '{self.title or self.url}' with {len(self.sections)} section(s) and {self.total_posts} post(s)"

    def to_markdown(self) -> str:
        """Convert the Padlet data to Markdown format.

        Note: Links are already inline as Markdown within post bodies.
        """
        lines = []

        if self.title:
            lines.append(f"# {self.title}\n")

        for section in self.sections:
            lines.append(f"## {section.title}\n")

            for post in section.posts:
                lines.append(f"### {post.subject}\n")
                lines.append(f"{post.body}\n")

        return "\n".join(lines)
