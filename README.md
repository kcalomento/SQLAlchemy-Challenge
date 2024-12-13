# **Climate API Project**

The **Climate API Project** offers an interface for accessing and analyzing weather data collected from Hawaii. Python, Flask, SQLAlchemy, and Pandas power the querying and data analysis functionalities.

---

## **Introduction**

The SQLAlchemy project analyzes and explores climate data for trip planning in Hawaii. Data on precipitation, temperature, and station activities is shown in a structured and accessible API. 

---

## **Analysis**

- Easy access to weather data via API routes.
- Historical precipitation, temperature, and station information.
- JSON responses for integration into external applications.
- Supports querying data ranges and specific stations for tailored results.

---

### **Tools**

The following tools are necessary for setup:

- Python 3.7+
- Flask
- SQLAlchemy
- Pandas

---

### **Setup Instructions**

1. **Clone the repository**:
    ```bash
    git clone https://github.com/kcalomento/SQLAlchemy-Challenge.git
    ```

2. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Start the application**:
    ```bash
    python app.py
    ```

4. **Access the API via your browser**:  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## **Routes Overview**

| **Route**                         | **Description**                                                             |
|------------------------------------|-----------------------------------------------------------------------------|
| `/`                                | Displays a list of all available routes.                                    |
| `/api/v1.0/precipitation`          | Provides precipitation data for the last year.                              |
| `/api/v1.0/stations`               | Returns a list of weather stations.                                         |
| `/api/v1.0/tobs`                   | Provides temperature observations for the most active station.              |
| `/api/v1.0/<start>`                | Displays min, avg, and max temperatures from the dataset's start date.      |
| `/api/v1.0/<start>/<end>`          | Shows temperature statistics for a specific date range within the last year.|
