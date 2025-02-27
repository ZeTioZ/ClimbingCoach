# ClimbingCoach - Augmented Reality for Climbing

## Overview

ClimbingCoach is an innovative application designed to enhance indoor climbing experiences using computer vision technologies. The application allows users to create climbing routes from photos of climbing walls, records their performance in real-time, and provides feedback to help climbers improve. By leveraging AI and AR, ClimbingCoach offers an immersive and educational experience for both beginners and experienced climbers.

## Features

### Route Creation and Performance Analysis
- **Route Creation**: Users can create climbing routes by uploading photos of climbing walls.
- **Real-Time Performance Tracking**: The application records and analyzes climbers' movements in real-time.
- **Feedback and Improvement**: Provides visual feedback on the climbing wall to help users correct and improve their techniques.

### Augmented Reality Integration
- **Immersive Experience**: Uses AR to project climbing routes and feedback directly onto the filmed climbing wall.
- **Interactive Learning**: Displays strategic information such as movement sequences, hold order, and support points to enhance learning.

### AI-Powered Pose Detection
- **YOLO-Pose**: Utilizes the YOLO (You Only Look Once) model for real-time human pose detection, ensuring high accuracy and speed.
- **Hold Detection**: Employs a YOLO-based model to detect climbing holds, enabling automated route creation and analysis.

### Cost-Effective Solution
- **Minimal Hardware Requirements**: Works with standard computers and webcams making it accessible and affordable.
- **Extensible Design**: The application is designed to be easily updated with new features via software updates.

## Technologies Used

### AI and Machine Learning
- **YOLO**: Used for real-time pose detection and hold identification.
- **RoboFlow**: For dataset management and model training.

### Augmented Reality
- **Computer Vision**: Analyzes climbers' movements and interactions with the wall.

### Software Development
- **Python**: The primary language for AI and backend development.

## Installation

### Prerequisites
- **Python**: Install Python 3.8 or higher.
- **Webcam**: For real-time video analysis.
  
### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ZefToZ/ClimbingCoach.git
   cd ClimbingCoach
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python ./src/gui.py
   ```

## Usage

### Creating a Climbing Route
1. **Upload a Photo**: Take a photo of the climbing wall and upload it to the application.
2. **Define Holds**: Use the application to mark the holds on the wall and define the route.
3. **Save the Route**: Save the route for future use or sharing.

### Real-Time Climbing Analysis
1. **Start Climbing**: Begin climbing the defined route.
2. **View Feedback**: The application will project real-time feedback onto the wall, showing your movements and suggesting improvements.

### Reviewing Performance
1. **Analyze Data**: After climbing, review detailed metrics such as completion percentage, total distance climbed, number of moves, and time taken.
2. **Adjust Routes**: Modify routes based on performance data to create more challenging or tailored climbing experiences.

## Future Improvements
- **Server Deployment**: Centralize requests and reduce hardware costs by deploying the application on a server.
- **Enhanced User Interface**: Optimize the user interface to better leverage YOLO's capabilities for a more intuitive experience.
- **Advanced AI Models**: Explore more advanced AI models for even more accurate pose and hold detection.

## Performance

### Dataset Comparison
| Dataset    | Size   | mAP (%) | Precision (%) | Recall (%) |
|------------|--------|---------|---------------|------------|
| Escalada [10]    | 176    | 96.1    | 97            | 90.4       |
| Holds Computer Vision Project [1] | 141    | 97.2    | 96.2          | 95.2       |
| Climbing Gym [3]    | 54     | 36      | 45.6          | 46.4       |
| Rock-Climbing-Hold-Detection [5] | 4282   | x       | x             | x          |
| Climbing Holds and Volumes [2] | 1717   | x       | x             | x          |

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is open-source and available under the MIT License.

## References
1. [Holds Dataset](https://universe.roboflow.com/betacaller/holds-9d06)
2. [Climbing Holds and Volumes Dataset](https://universe.roboflow.com/blackcreed-sypgh/climbing-holds-and-volumes)
3. [Climbing Gym Dataset](https://universe.roboflow.com/cassie-kilda/climbing-gym)
4. [Rock-Climbing-Hold-Detection Dataset](https://universe.roboflow.com/gdscmoombess/rock-climbing-hold-detection)
5. [Escalada Dataset](https://universe.roboflow.com/jaan-rodriguez-jannik/escalada)

## Demonstration Video
Watch the demonstration video [here](https://youtu.be/FeVorggcMlA).
