import obd
import sys
from subprocess import call
import time
from pathlib import Path

from PyQt5 import QtCore as qTC
from PyQt5 import QtGui as qTG
from PyQt5 import QtWidgets as qTW
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize


# Convert kph to mph
def convert_MPH(kph):
    return kph * 0.62137119


# Convert ℃ to ℉
def convert_degrees(deg_celsius):
    return (deg_celsius * 9 / 5) + 32


class DigitalDashWindow(qTW.QWidget):
    # authenticated = qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set Background Image
        self.image = qTG.QImage("resources/background_day.jpg")
        self.palette = qTG.QPalette()
        self.palette.setBrush(qTG.QPalette.Window, qTG.QBrush(self.image))
        self.setPalette(self.palette)

        # Set window size
        self.resize(800, 480)

        # GUI Layout Base Layer
        self.grid_layout_widget = qTW.QWidget(self)
        self.grid_layout_widget.setGeometry(0, 0, 800, 480)
        grid_layout = qTW.QGridLayout(self.grid_layout_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        vertical_center = qTW.QVBoxLayout()
        vertical_center.setSpacing(0)

        # Speedometer Value
        self.speed_value = qTW.QLabel(self.grid_layout_widget)
        self.speed_value.setObjectName("speed_value")
        self.speed_value.setText("0")
        self.speed_value.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.speed_value.setMargin(-31)
        self.speed_value.setMaximumHeight(160)
        vertical_center.addWidget(self.speed_value)

        # Speedometer Label
        self.speed_label = qTW.QLabel(self.grid_layout_widget)
        self.speed_label.setObjectName("speed_label")
        self.speed_label.setText("MPH")
        self.speed_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.speed_label.setMargin(-10)
        self.speed_label.setIndent(-1)
        self.speed_label.setMaximumHeight(75)
        vertical_center.addWidget(self.speed_label)

        warnings_hbox = qTW.QHBoxLayout()

        # First Warning Spacer
        self.spacer = qTW.QLabel(self.grid_layout_widget)
        self.spacer.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.spacer_pix = qTG.QPixmap("resources/empty.png")
        self.spacer.setPixmap(self.spacer_pix)
        self.spacer.setScaledContents(True)
        self.spacer.setFixedSize(60, 60)
        warnings_hbox.addWidget(self.spacer)

        # Battery Warning
        self.battery = qTW.QLabel(self.grid_layout_widget)
        self.battery.setObjectName("battery")
        self.battery.setText("Battery")
        self.battery.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.battery_active_pix = qTG.QPixmap("resources/battery.png")
        self.battery_inactive_pix = qTG.QPixmap("resources/empty.png")
        self.battery.setPixmap(self.battery_inactive_pix)
        self.battery.setScaledContents(True)
        self.battery.setFixedSize(50, 50)
        warnings_hbox.addWidget(self.battery)

        # Check Engine Light
        self.check_engine = qTW.QLabel(self.grid_layout_widget)
        self.check_engine.setObjectName("check_engine")
        self.check_engine.setText("Check Engine")
        self.check_engine.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.cel_active_pix = qTG.QPixmap("resources/cel.png")
        self.cel_inactive_pix = qTG.QPixmap("resources/empty.png")
        self.check_engine.setPixmap(self.cel_inactive_pix)
        self.check_engine.setScaledContents(True)
        self.check_engine.setFixedSize(50, 50)
        warnings_hbox.addWidget(self.check_engine)

        # Airbag Warning
        self.airbag = qTW.QLabel(self.grid_layout_widget)
        self.airbag.setObjectName("airbag")
        self.airbag.setText("Airbag")
        self.airbag.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.airbag_active_pix = qTG.QPixmap("resources/airbag.png")
        self.airbag_inactive_pix = qTG.QPixmap("resources/empty.png")
        self.airbag.setPixmap(self.airbag_inactive_pix)
        self.airbag.setScaledContents(True)
        self.airbag.setFixedSize(50, 50)
        warnings_hbox.addWidget(self.airbag)

        # Second Spacer
        warnings_hbox.addWidget(self.spacer)

        vertical_center.addLayout(warnings_hbox)
        center_bottom = qTW.QHBoxLayout()
        center_bottom.setSpacing(0)
        vertical_center.addLayout(center_bottom)

        # Clock
        self.clock = qTW.QLabel(self.grid_layout_widget)
        self.clock.setObjectName("clock")
        self.clock.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.clock.setMargin(10)
        center_bottom.addWidget(self.clock)

        grid_layout.addLayout(vertical_center, 0, 1, 1, 1)
        vertical_left = qTW.QVBoxLayout()
        vertical_left.setSpacing(0)
        vertical_left.setObjectName("verticalLeft")
        left_top = qTW.QHBoxLayout()
        left_top.setSpacing(0)
        left_top.setObjectName("leftTop")
        v_left_top = qTW.QVBoxLayout()
        v_left_top.setObjectName("v_left_top")

        # Left Turn Signal
        self.left_turn = qTW.QLabel(self.grid_layout_widget)
        self.left_turn.setObjectName("left_turn")
        self.left_active_pix = qTG.QPixmap("resources/left.png")
        self.left_inactive_pix = qTG.QPixmap("resources/left_inactive.png")
        self.left_turn.setPixmap(self.left_inactive_pix)
        self.left_turn.setScaledContents(True)
        self.left_turn.setFixedSize(100, 100)
        v_left_top.addWidget(self.left_turn)

        # Fuel Gauge (to be implemented later)
        self.fuel = qTW.QLabel(self.grid_layout_widget)
        self.fuel.setObjectName("fuel")
        # self.fuel.setText("Fuel Gauge")
        self.fuel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        v_left_top.addWidget(self.fuel)

        left_top.addLayout(v_left_top)
        vertical_left.addLayout(left_top)

        # RPM Value
        self.rpm_value = qTW.QLabel(self.grid_layout_widget)
        self.rpm_value.setObjectName("rpm_value")
        self.rpm_value.setText("0")
        self.rpm_value.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.rpm_value.setMargin(-10)
        vertical_left.addWidget(self.rpm_value)

        # RPM Label
        self.rpm_label = qTW.QLabel(self.grid_layout_widget)
        self.rpm_label.setObjectName("rpm_label")
        self.rpm_label.setText("RPM")
        self.rpm_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.rpm_label.setMargin(0)
        vertical_left.addWidget(self.rpm_label)

        left_bottom = qTW.QHBoxLayout()
        left_bottom.setSpacing(0)
        left_bottom.setObjectName("leftBottom")

        # Settings Button
        self.settings = qTW.QPushButton(self.grid_layout_widget)
        self.settings.setObjectName("pushButton")
        settings_icon = qTG.QIcon("resources/settings.png")
        self.settings.setFlat(True)  # Make button transparent
        self.settings.setFixedSize(150, 100)
        self.settings.setIcon(settings_icon)
        self.settings.setIconSize(QSize(50, 50))
        left_bottom.addWidget(self.settings)

        vertical_left.addLayout(left_bottom)
        grid_layout.addLayout(vertical_left, 0, 0, 1, 1)
        vertical_right = qTW.QVBoxLayout()
        vertical_right.setSpacing(0)
        vertical_right.setObjectName("verticalRight")
        right_top = qTW.QHBoxLayout()
        right_top.setSpacing(0)
        right_top.setObjectName("rightTop")
        v_right_top = qTW.QVBoxLayout()
        v_right_top.setObjectName("v_right_top")
        h_right_top = qTW.QHBoxLayout()
        h_right_top.setObjectName("horizontal_top_right")

        # Headlight Indicators
        self.headlights = qTW.QLabel(self.grid_layout_widget)
        self.headlights.setObjectName("headlights")
        self.headlights.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.headlights_low_pix = qTG.QPixmap("resources/low-beam.png")
        self.headlights_high_pix = qTG.QPixmap("resources/high-beam_blue.png")
        self.headlights_inactive_pix = qTG.QPixmap("resources/empty.png")
        self.headlights.setPixmap(self.headlights_inactive_pix)
        self.headlights.setScaledContents(True)
        self.headlights.setFixedSize(50, 50)
        h_right_top.addWidget(self.headlights)

        # Right Turn Signal
        self.right_turn = qTW.QLabel(self.grid_layout_widget)
        self.right_turn.setObjectName("right_turn")
        self.right_turn.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.right_active_pix = qTG.QPixmap("resources/right.png")
        self.right_inactive_pix = qTG.QPixmap("resources/right_inactive.png")
        self.right_turn.setPixmap(self.right_inactive_pix)
        self.right_turn.setScaledContents(True)
        self.right_turn.setFixedSize(100, 100)
        h_right_top.addWidget(self.right_turn)

        v_right_top.addLayout(h_right_top)

        # Oil Pressure Gauge (future implementation)
        self.oil = qTW.QLabel(self.grid_layout_widget)
        self.oil.setObjectName("oil")
        self.oil.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        # self.oil.setText("Oil Pressure")
        v_right_top.addWidget(self.oil)

        right_top.addLayout(v_right_top)
        vertical_right.addLayout(right_top)

        # Coolant Temp
        self.temp_value = qTW.QLabel(self.grid_layout_widget)
        self.temp_value.setObjectName("temp_value")
        self.temp_value.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.temp_value.setText("0°")
        self.temp_value.setMargin(-10)
        vertical_right.addWidget(self.temp_value)

        # Coolant Temp Label
        self.temp_label = qTW.QLabel(self.grid_layout_widget)
        self.temp_label.setObjectName("temp_label")
        self.temp_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.temp_label.setText("COOLANT")
        self.temp_label.setMargin(0)
        vertical_right.addWidget(self.temp_label)

        right_bottom = qTW.QHBoxLayout()
        right_bottom.setSpacing(0)
        right_bottom.setObjectName("rightBottom")

        # Night Mode Button
        self.night_mode_bool = False  # False for day, True for Night
        self.night_mode = qTW.QPushButton(self.grid_layout_widget)
        night_mode_icon = qTG.QIcon("resources/night_mode.png")
        self.night_mode.setFlat(True)  # Make button transparent
        self.night_mode.setFixedSize(150, 100)
        self.night_mode.setIcon(night_mode_icon)
        self.night_mode.setObjectName("night_mode")
        self.night_mode.setIconSize(QSize(50, 50))
        right_bottom.addWidget(self.night_mode)

        vertical_right.addLayout(right_bottom)
        grid_layout.addLayout(vertical_right, 0, 2, 1, 1)

        # Make Dashboard a frameless window
        self.flags = qTC.Qt.WindowFlags(qTC.Qt.FramelessWindowHint)  # | qTC.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.flags)

        # Implement the .qss stylesheet
        self.theme = open('theme.qss').read()
        self.setStyleSheet(self.theme)

        # Initialize connection to ELM327 device
        self.connection = obd.Async()

        # Loop until connection is found
        # while self.connection.status() == OBDStatus.NOT_CONNECTED:
        #    self.connection = obd.Async()
        #    time.sleep(3)  # Wait 3 sec to try again

        # print('Connected!')  # ELM327 found

        # OBD Lookup Commands
        rpm = obd.commands.RPM
        speed = obd.commands.SPEED
        temp = obd.commands.COOLANT_TEMP
        cel_status = obd.commands.STATUS

        # Async commands to watch and callback methods
        self.connection.watch(rpm, callback=self.new_rpm)
        self.connection.watch(speed, callback=self.new_speed)
        self.connection.watch(temp, callback=self.new_temp)
        self.connection.watch(cel_status, callback=self.new_cel_status)

        # Begin Scan and Display DigitalDashWindow
        self.connection.start()

        self.night_mode.clicked.connect(lambda: self.switch_day_night())
        self.settings.clicked.connect(lambda: self.showSettingsDialog())

        # Timer for updating clock display
        self.timer = qTC.QTimer(self)
        self.timer.timeout.connect(lambda: self.update_clock())
        self.timer.start(1000)  # Update once per second

        self.show()  # Show DigitalDashWindow

    # Catch and handle key press events
    def keyPressEvent(self, event):
        # Exit when Escape is pressed
        if event.key() == Qt.Key_Escape:
            exit(self)
        # Shutdown the system when 'S' is pressed
        if event.key() == Qt.Key_S:
            call("sudo poweroff", shell=True)  # Shutdown the Pi
        # Light up left turn signal
        if event.key() == Qt.Key_A:
            self.left_turn.setPixmap(self.left_active_pix)
        # Light up right turn signal
        if event.key() == Qt.Key_D:
            self.right_turn.setPixmap(self.right_active_pix)
        # Light up battery warning
        if event.key() == Qt.Key_1:
            self.battery.setPixmap(self.battery_active_pix)
        # Light up Check Engine warning
        if event.key() == Qt.Key_2:
            self.check_engine.setPixmap(self.cel_active_pix)
        # Light up airbag warning
        if event.key() == Qt.Key_3:
            self.airbag.setPixmap(self.airbag_active_pix)
        # Light up low beam notification
        if event.key() == Qt.Key_4:
            self.headlights.setPixmap(self.headlights_low_pix)
        # Light up high beam notification
        if event.key() == Qt.Key_5:
            self.headlights.setPixmap(self.headlights_high_pix)

    # Catch and handle key release events
    def keyReleaseEvent(self, event):
        # Turn off left turn signal
        if event.key() == Qt.Key_A:
            self.left_turn.setPixmap(self.left_inactive_pix)
        # Turn off right turn signal
        if event.key() == Qt.Key_D:
            self.right_turn.setPixmap(self.right_inactive_pix)
        # Turn off battery warning
        if event.key() == Qt.Key_1:
            self.battery.setPixmap(self.battery_inactive_pix)
        # Turn off check engine warning
        if event.key() == Qt.Key_2:
            self.check_engine.setPixmap(self.cel_inactive_pix)
        # Turn off airbag warning
        if event.key() == Qt.Key_3:
            self.airbag.setPixmap(self.airbag_inactive_pix)
        # Turn off low beam notification
        if event.key() == Qt.Key_4:
            self.headlights.setPixmap(self.headlights_inactive_pix)
        # Turn off high beam notification
        if event.key() == Qt.Key_5:
            self.headlights.setPixmap(self.headlights_inactive_pix)

    # Toggle Day/Night Mode by changing background
    def switch_day_night(self):
        if not self.night_mode_bool:
            self.night_mode_bool = True
            # self.night_mode.setText("Day Mode")
            self.image = qTG.QImage("resources/background_night.jpg")
            self.palette = qTG.QPalette()
            self.palette.setBrush(qTG.QPalette.Window, qTG.QBrush(self.image))
            self.setPalette(self.palette)
        else:
            self.night_mode_bool = False
            # self.night_mode.setText("Night Mode")
            self.image = qTG.QImage("resources/background_day.jpg")
            self.palette = qTG.QPalette()
            self.palette.setBrush(qTG.QPalette.Window, qTG.QBrush(self.image))
            self.setPalette(self.palette)

    # Update the Dash Clock from the system clock
    def update_clock(self):
        current_time = qTC.QTime.currentTime()
        display_time = current_time.toString('h:mm AP')
        self.clock.setText(display_time)

    # Callback Method for Updating RPMs
    def new_rpm(self, revs):
        value = revs.value
        rpm = int(value.magnitude)
        if value.magnitude:
            self.rpm_value.setText(f'{rpm}')
        else:
            self.rpm_value.setText(f'0')

    # Callback Method for Updating Speed
    def new_speed(self, kph):
        value = kph.value
        mph = convert_MPH(value.magnitude)
        mph = int(mph)
        if value.magnitude:
            self.speed_value.setText(f'{mph}')
        else:
            self.speed_value.setText(f'0')

    # Callback Method for Updating Coolant Temp
    def new_temp(self, deg):
        value = deg.value
        deg_f = convert_degrees(value.magnitude)
        deg_f = int(deg_f)
        if value.magnitude:
            self.temp_value.setText(f'{deg_f}°')
        else:
            self.temp_value.setText(f'Unknown')

    # Callback Method for Updating Coolant Temp
    def new_cel_status(self, status):
        cel_bool = status.value.MIL
        if cel_bool:
            self.check_engine.setPixmap(self.cel_active_pix)
        else:
            self.check_engine.setPixmap(self.cel_inactive_pix)

    # Open Settings Dialog Box
    def showSettingsDialog(self):
        dialog = qTW.QDialog()
        dialog.setWindowFlags(self.flags)
        dialog.resize(800, 480)
        dialog.setStyleSheet(self.theme)
        dialog.setWindowOpacity(0.9)

        # Save Settings
        save_button = qTW.QPushButton("Save", dialog)
        save_button.setObjectName("save_button")
        save_button.setFlat(True)
        save_button.move(280, 400)
        save_button.clicked.connect(lambda: dialog.accept())

        # Close without saving
        close_button = qTW.QPushButton("Close", dialog)
        close_button.setFlat(True)
        close_button.move(420, 400)
        close_button.clicked.connect(lambda: dialog.reject())

        dialog.setWindowTitle("Settings")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


# Opening Splash Screen Animation Class
class MovieSplashScreen(qTW.QSplashScreen):
    def __init__(self, video):
        video.jumpToFrame(0)
        pixmap = qTG.QPixmap(video.frameRect().size())

        qTW.QSplashScreen.__init__(self, pixmap)
        self.movie = video
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, event):
        self.movie.start()

    def hideEvent(self, event):
        self.movie.stop()

    def paintEvent(self, event):
        painter = qTG.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize()


if __name__ == '__main__':
    app = qTW.QApplication(sys.argv)

    # Install all the fonts (may need to be installed on host system as well...)
    fonts = Path("resources/fonts")
    for file in fonts.glob('*.otf'):
        # print(file.name)
        qTG.QFontDatabase.addApplicationFont(file.name)

    # widget = DigitalDashWindow(windowTitle='Digital Dashboard')

    # Initialize splash video/animation
    movie = qTG.QMovie("resources/black_bear.gif")
    splash = MovieSplashScreen(movie)
    splash.show()
    start = time.time()
    while movie.state() == qTG.QMovie.Running and time.time() < start + 4.4:
        app.processEvents()

    widget = DigitalDashWindow(windowTitle='Digital Dashboard')
    splash.finish(widget)  # Exit splash to the main dashboard
    sys.exit(app.exec_())
