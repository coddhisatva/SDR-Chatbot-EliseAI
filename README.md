# EliseAI Practical Interview

## Interview Format

The interview will follow this structure:

```
T0:         Interview Start - Interviewer to give ~5-10 minute description of the problem 
T0 + 30:    First Check-in 
T0 + 60:    Second Check-in
T1 - 15:    Presentation
T1:         Interview End
```
If you are completing the practical virtually, please remain in the scheduled Google Meet. Your interviewer will join at the designated times.

The final 15 minutes will be a presentation where you'll showcase what you've built. You’re free to present what you think is most relevant, but suggested topics include:

- Walkthrough of features and your overall approach
- Justification for impactful decisions
- What you would do with more time

## Overview

In this assessment, you'll build an AI-powered Sales Development Representative (SDR) chatbot for EliseAI, a Series D property management tech company leveraging AI to enhance housing and real estate operations.

## The Challenge

Your task is to create a conversational AI assistant that can:

1. Retrieve and understand content from EliseAI's blog
2. Simulate an SDR (Sales Development Representative) by leveraging this content
3. Engage potential customers, understand their needs, and pitch EliseAI’s solutions
4. Maintain a natural, engaging conversation with effective sales techniques

## EliseAI Product Overview
Your chatbot should be knowledgeable about these core EliseAI products:

1. **LeasingAI**: An AI assistant that handles prospect inquiries 24/7, schedules tours, answers questions about pricing and amenities, and helps boost lead-to-lease rates.

2. **MaintenanceAI**: Streamlines the maintenance workflow through AI-powered technician assignment, work order management, and integration with property management systems.

3. **DelinquencyAI**: Automatically sends payment reminders, follows up on outstanding payments, and helps reduce delinquency rates.

4. **LeaseAudits**: Helps ensure lease compliance and accuracy through automated review processes.

5. **EliseCRM**: A comprehensive CRM platform that serves as a hub for prospect and resident information, reporting, and operational workflows.


## Implementation Guidelines

Your solution should include:

1. **Knowledge Processing** – Convert content into a usable knowledge base
2. **Chat Interface** – Chat UI for user interaction. Aim above and beyond a simple UI, the more helpful features to achieve our goal of a sale, the better!
3. **SDR Behavior** – Bot should introduce itself, ask relevant questions, explain offerings, and aim to book a demo

## Technical Notes

- The reference bot was built with GPT-4o-mini; the provided budget should suffice
- Store blog content in a structured, retrievable format
- Prioritize a helpful, natural, and persuasive conversation flow

## Tools & Assistance

**Use all tools at your disposal!** We encourage use of:

- AI assistants (ChatGPT, Claude, etc.)
- Code environments (Cursor IDE, VSCode, etc.)
- Code completion tools (GitHub Copilot, etc.)
- Any other productivity tools that help you work effectively
- Database visualizers or VSCode extensions (SQLite, etc.)

This is not only allowed—it’s expected. We want to see how you leverage tools to solve real-world problems.

## Submission Requirements

Please submit:

1. All source code
2. A README with:
   - Setup instructions
   - Brief explanation of your approach
   - Notable challenges and solutions
   - How you'd improve the bot with more time

## Evaluation Criteria

We’ll evaluate your solution based on:

- Functionality and completeness
- Code quality and structure
- SDR bot performance in conversations
- Creativity and problem-solving
- Efficient tool usage

## Running the App

This will start the complete stack including the database, backend API, and React frontend.

```
docker-compose up
```

By default, the front-end will be accessible at http://localhost:3000 and the back-end at http://localhost:8000.


### Project Structure

```
├── articles/               # Folder of JSON blog articles with the format: title, author, date, summary, main_content (Markdown formatted) 
├── backend/                # Python FastAPI app
│   ├── app.py              # API router and endpoints
│   ├── db.py               # Database connection and query utilities
│   ├── .env                # Environment variables including API keys
│   ├── Dockerfile          # Docker configuration for backend
│   └── requirements.txt    # Python dependencies
│
├── database/               # Database 
│   ├── data/               
│   │   └── practical.db    # SQLite database file - Only populated after initialization
│   └── init/               
│       └── init.sql        # SQL initialization script
│
├── frontend/               # React app with Tailwind CSS
│   ├── src/                
│   │   ├── App.jsx         # Main React component
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       
│   ├── public/             # Static files
│   ├── package.json        
│   ├── tailwind.config.js  
│   ├── postcss.config.js   
│   ├── vite.config.js      # Vite configuration with API proxying
│   └── Dockerfile          
│
├── docker-compose.yml      # Docker configuration for all services
├── Dockerfile              # Main Dockerfile for single container deployment
├── .gitignore              
└── README.md               # Project documentation
```

_________


i should be able to type in text box even when ai is typing