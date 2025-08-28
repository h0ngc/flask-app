# Video Review Pipeline

## Overview

This is a local single-page web application that orchestrates a 3-step video review pipeline. The system allows users to pull data, create video descriptions with product information, and run judgements on video content. Results are displayed categorized by Yes/N/A/No responses. The application features a Flask API backend that manages data storage and processing across 12 different AI model variants, with a responsive frontend that maintains state and provides real-time interaction with the pipeline.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology Stack**: Pure HTML, CSS, and JavaScript (no bundlers required)
- **Single-Page Application**: Routes/sections change without page reloads
- **State Management**: In-memory state with localStorage persistence for active UUID
- **Responsive Design**: Modern, clean UI with sticky global header
- **Model Selection**: Segmented control or searchable dropdown for 12 model variants

### Backend Architecture
- **Framework**: Flask with CORS enabled for cross-origin requests
- **API Design**: RESTful JSON API running on localhost:8000
- **Data Storage**: File-based system using organized directory structure
- **UUID-based Organization**: Each session/pipeline run gets a unique UUID
- **Model Support**: 12 distinct AI model variants with separate data paths

### Data Storage Solution
- **Structure**: Hierarchical file system under `data/` directory
- **Organization**: `data/{uuid}/{model_name}/{csv_files}`
- **File Types**: CSV files for storing pipeline results and intermediate data
- **Directory Management**: Automatic creation of model-specific directories
- **Data Persistence**: Local file system storage without database dependency

### Pipeline Architecture
- **3-Step Process**: 
  1. Data pulling
  2. Video description and product info creation
  3. Judgement execution
- **Model Variants**: Support for both Qwen and Smol models with CoT (Chain of Thought) and direct variants
- **Data Types**: Video image info/raw, description info processing
- **Result Categorization**: Yes/N/A/No classification system

### State Management
- **Session Persistence**: Active UUID stored in localStorage
- **Model Selection**: Dynamic switching between 12 model variants
- **Date Handling**: Asia/Seoul timezone with days-back filtering
- **Real-time Updates**: Immediate UI updates on model/parameter changes

## External Dependencies

### Frontend Dependencies
- **Font Awesome 6.0.0**: Icon library from CDN for UI elements
- **Browser APIs**: localStorage for persistence, Date API for timezone handling

### Backend Dependencies
- **Flask**: Web framework for API endpoints
- **Flask-CORS**: Cross-origin resource sharing support
- **Python Standard Library**: 
  - `pathlib` for file system operations
  - `uuid` for unique identifier generation
  - `json` and `csv` for data serialization
  - `logging` for application monitoring

### Development Environment
- **No Authentication**: Local development setup without user management
- **Docker Support**: Backend designed to run in Docker container
- **Hot Reload**: Debug mode enabled for development
- **Port Configuration**: Fixed on port 8000 for consistent frontend integration