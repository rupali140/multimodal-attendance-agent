# Technical Architecture

## 1. Architecture Overview

The application follows a modular architecture with a Streamlit interface and independent processing modules.

## 2. Components

### Presentation Layer
Streamlit dashboard for attendance records, session analytics, and recommendations.

### Vision Module
Processes supported video input to detect and track participants and produce attendance-related observations.

### Audio Module
Processes supported audio input to extract session-level activity indicators.

### Engagement Analysis Module
Combines available vision and audio indicators to calculate cautious engagement estimates.

### Recommendation Module
Converts validated session patterns into explainable teaching suggestions.

### Data Layer
Manages attendance records and derived analytics with appropriate privacy safeguards.

## 3. Data Flow

Video and audio inputs
→ Vision and audio processing
→ Feature validation and aggregation
→ Engagement analysis
→ Recommendation generation
→ Streamlit dashboard

Attendance records are managed as a related workflow and may be associated with session summaries when appropriate.

## 4. Initial Technology Choices
- Python 3.12
- Streamlit
- Pandas
- Plotly
- OpenCV, to be introduced during Epic 2
- An audio-processing library, to be selected during Epic 3

## 5. Design Principles
- Modular separation of concerns
- Local-first processing where practical
- Input validation and graceful error handling
- Explainable outputs
- Privacy-conscious storage
- Independent module testing
