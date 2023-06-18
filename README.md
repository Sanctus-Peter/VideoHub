# Video Hub Project

![Repo size](https://img.shields.io/github/repo-size/Sanctus-Peter/VideoHub)
![Pep8 style](https://img.shields.io/badge/PEP8-style%20guide-purple?style=round-square)
![Latest commit](https://img.shields.io/github/last-commit/Sanctus-Peter/VideoHub/main?style=round-square)
![License](https://img.shields.io/github/license/Sanctus-Peter/VideoHub?style=round-square)


VideoHub is a web application built with FastAPI that allows users to manage and organize their video library.

## Description

VideoHub provides a user-friendly interface to upload, organize, and watch videos. It allows users to create collections, add videos to collections, and search for videos based on different criteria. The application also supports user authentication and authorization to ensure secure access to the video library.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)
- [Support](#support)
- [Roadmap](#roadmap)
- [Changelog](#changelog)


## Features

- **FastAPI Backend**: The backend of the Video Hub is powered by FastAPI, a modern and high-performance web framework. It provides seamless video upload, management, and retrieval, with asynchronous capabilities for optimal performance and responsiveness.

- **NoSQL Cassandra Database**: The Video Hub leverages the scalability and resilience of NoSQL Cassandra database. This distributed database ensures fault tolerance and enables seamless horizontal scaling as the platform expands.

- **Frontend with HTML/CSS, JavaScript, and Bootstrap**: The Video Hub project offers a sleek and intuitive user interface. With clean HTML/CSS code and dynamic interactivity powered by JavaScript, the platform delivers a seamless and enjoyable video browsing experience across various devices. Bootstrap framework is used for responsive design and component styling.

- **Jinja2 Templating**: The Video Hub incorporates the Jinja2 template engine, enabling dynamic content generation and efficient rendering. This allows for customization and personalization of the user interface.

- **Algolia Search Integration**: Algolia search functionality is integrated into the Video Hub platform, enhancing the discoverability of video content. Users can easily find specific videos using search queries, thanks to Algolia's powerful search capabilities and intelligent ranking algorithms.

- **Authentication and Authorization**: The Video Hub platform is secured with authentication and authorization. Users can create accounts and log in to the platform. The platform also supports role-based access control, with different levels of access for users and administrators.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/Sanctus-Peter/VideoHub.git
cd VideoHub
```
2. Create a virtual environment and activate it:

```shell
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install the dependencies:

```shell
pip install -r requirements.txt
```

## Usage

1. create a free account on [cassandra cloud](https://astra.datastax.com/) and get the connection details
2. Configure the Cassandra database connection settings in config.py:
3. Start the FastAPI server:

```shell
uvicorn api.v1.app.main:app --reload
```
4. Open the application in your browser at http://localhost:8000
