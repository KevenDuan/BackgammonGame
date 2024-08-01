import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('任务执行界面')
        self.setGeometry(300, 300, 400, 300)
        self.layout = QVBoxLayout()

        self.label = QLabel("请选择你的任务代码：", self)
        self.layout.addWidget(self.label)

        # 创建五个按钮
        for i in range(5):
            button = QPushButton(f'执行任务 {i + 1}', self)
            button.clicked.connect(lambda checked, task=i: self.executeTask(task))
            self.layout.addWidget(button)

        self.setLayout(self.layout)
        self.show()

    def executeTask(self, task_number):
        # 根据任务编号选择要执行的程序
        task_script = f'main{task_number + 1}.py'  # 假设脚本名为 task_1.py, task_2.py 等
        try:
            # 执行外部 Python 程序
            result = subprocess.run(['python', task_script], capture_output=True, text=True)
            if result.returncode == 0:
                QMessageBox.information(self, "任务完成", f"任务 {task_number + 1} 执行完成！\n输出:\n{result.stdout}")
            else:
                QMessageBox.warning(self, "任务失败", f"任务 {task_number + 1} 执行失败！\n错误输出:\n{result.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"执行任务时发生错误: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    sys.exit(app.exec_())