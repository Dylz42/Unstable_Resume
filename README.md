# Unstable Resume

**An AI-powered resume tailoring web application built using Python, Flask, OpenAI, Pydantic, and Jinja2.**

## Overview

Computer Science is an incredibly broad field, with hundreds of unique career paths, specialisations, and opportunities. Having studied a wide range of subjects and developed skills across multiple disciplines, I found that applying for different positions often required creating multiple versions of my resume to highlight the most relevant qualifications and experience.

This led me to a simple question: **Why not create a single master resume and automatically tailor it to a job description?**

Introducing **Unstable Resume!**

Unstable Resume is a web application that stores a comprehensive master resume containing all my qualifications, technical skills, education, projects, and professional experience. By providing a job description, the application uses OpenAI's API to identify and prioritise the most relevant information, generating a tailored resume suitable for the position.

For example, when applying for a Data Science position, skills involving Excel, Tableau, Python, and data analysis would be highly relevant. However, experience using CAD software such as Fusion 360 might not be particularly useful to that employer.

Rather than manually rewriting my resume for every application, Unstable Resume automatically prioritises relevant information, allowing employers to quickly identify the skills and experience most applicable to their position.

## How It Works

The application follows a straightforward process:

1. **Master Resume:** A JSON file stores comprehensive information about my education, qualifications, technical skills, projects, and professional experience.
2. **Job Description:** The user enters a job description through the Flask web application's interface.
3. **AI Processing:** The application sends the job description and relevant master resume information to OpenAI's API to identify and prioritise applicable skills, coursework, and qualifications.
4. **Structured Output:** Pydantic models define the expected AI response, ensuring the returned information follows a predictable structure that the application can process.
5. **Validation:** The application performs additional checks against the master resume to minimise the possibility of fabricated skills or qualifications.
6. **Resume Generation:** Flask and Jinja2 dynamically render the tailored information into an HTML resume, styled using CSS and formatted for printing or saving as a PDF.

## Technical Implementation

This project represents a natural progression from my previous applications, combining familiar technologies with new concepts and development challenges.

**Python and Flask**

Building on my experience developing [DexGuess](https://github.com/Dylz42), I used Python and Flask to create the web application's backend, handle user input, manage application logic, and render dynamic pages.

**HTML, CSS, and Jinja2**

One of the most important components of this project is Jinja2, which allows the application to dynamically populate HTML templates with information from the master resume.

Rather than manually constructing a resume for each application, the program uses reusable templates to generate a consistent layout regardless of the information selected.

CSS is used to create a professional, printable resume with formatting specifically designed for A4 pages and PDF output.

**OpenAI API**

Building on my experience working with APIs in my [NASA APOD Wallpaper](https://github.com/Dylz42/NASA_POTD_Wallpaper) application, I integrated OpenAI's API to analyse job descriptions and identify relevant resume information.

Unlike a conventional API that returns predetermined data, generative AI introduces additional challenges involving response consistency, accuracy, and validation.

**Pydantic and JSON**

This project introduced me to Pydantic, which I used to define structured models for OpenAI's responses.

The master resume is stored in JSON format, allowing information to be organised into reusable categories and accessed programmatically.

Together, these technologies provide a flexible foundation for generating tailored resumes while maintaining control over the information being displayed.

## Development Challenges and Solutions

Although the project builds upon skills developed in my previous applications, integrating generative AI introduced several new challenges.

### 1. Structuring AI Responses

**Challenge:** Generative AI can produce responses with varying structures, making it difficult to reliably process the returned information.

**Solution:** I implemented Pydantic models to define the expected response structure, including tailored education, skill categories, and professional summaries.

This allows the application to work with predictable Python objects rather than attempting to interpret unstructured AI-generated text.

### 2. Minimising AI Hallucinations

**Challenge:** When generating professional documents, accuracy is essential. AI-generated resumes must not invent qualifications, technical skills, or experience that the applicant does not possess.

**Solution:** I introduced validation checks that compare AI-selected information against the original master resume.

By restricting the application to information already provided in the master resume, I aimed to minimise hallucinations and maintain the accuracy of the generated document.

### 3. Maintaining a Consistent Resume Layout

**Challenge:** Different job descriptions produce different amounts of relevant information, making it difficult to maintain a consistent and professional resume layout.

**Solution:** I implemented word count restrictions, content limits, and CSS print formatting to control the amount of information displayed.

I also used Jinja2 templates to dynamically render resume sections, allowing the layout to accommodate different combinations of skills, coursework, and experience.

These measures help maintain a readable two-page resume while avoiding unnecessary formatting issues during PDF generation.

## Future Improvements

Although the core application is functional, there are several features I would like to implement as the project develops.

- **GitHub Integration:** Allow the application to retrieve information from my GitHub repositories and automatically populate the projects section with relevant technical details.
- **Single-Page Resume Generation:** Introduce an option to condense the generated resume into a one-page format for employers who prefer shorter applications.
- **Custom Master Resumes:** Allow individual users to upload or create their own master resume files, making the application accessible without requiring modifications to the source code.
- **Improved User Interface:** Redesign the application's homepage to provide a more polished and intuitive experience while maintaining its simplicity.
- **AI Transparency:** Introduce a small indicator or disclaimer identifying the use of AI-assisted resume tailoring.
- **Further Validation:** Continue improving the accuracy and reliability of the AI-generated content to ensure that resumes remain faithful to the information provided.

## AI Usage During Development

Generative AI was used throughout the development of Unstable Resume as a learning and development tool.

In particular, I consulted AI to better understand the OpenAI API, explore structured outputs using Pydantic, develop the resume's CSS layout, and organise the master resume JSON file.

AI was also useful for discussing implementation approaches, troubleshooting errors, and exploring solutions to challenges involving response validation and document formatting.

This project gave me an opportunity to explore generative AI not only as a development assistant but also as a core component of a practical application.

By combining conventional programming techniques with generative AI, I gained a better understanding of how large language models can be integrated into software applications while maintaining structured outputs, validation, and control over the final results.
