def get_css():
    return """
        <style>
        .main {
            padding: 2rem;
            background-color: var(--background-color);
        }
        .stButton > button {
            width: 100%;
            padding: 0.5rem;
            border-radius: 15px;
            font-size: 1.2rem;
        }
        .story-container {
            background-color: var(--background-color);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 1rem;
        }
        .title-container {
            background: linear-gradient(90deg, #70a1ff, #7bed9f);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .parameter-card {
            background-color: var(--background-color);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .sidebar-content {
            background-color: var(--background-color);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        }
        .sidebar-content p {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        </style>
    """