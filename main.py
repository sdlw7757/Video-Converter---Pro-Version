#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转音频工具 - 主程序
功能：视频转MP3
作者：AI Assistant
"""

import sys
import os
import subprocess
import threading
import json
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QProgressBar, QTextEdit, QComboBox, QCheckBox,
                             QGroupBox, QMessageBox, QTabWidget, QListWidget,
                             QListWidgetItem, QSplitter, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QMimeData
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QDragEnterEvent, QDropEvent

class DraggableLabel(QLabel):
    """支持拖拽的标签组件"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QLabel {
                padding: 8px;
                background-color: white;
                border: 2px dashed #ccc;
                border-radius: 3px;
                color: #666;
            }
            QLabel:hover {
                border-color: #4CAF50;
                background-color: #f0f8f0;
            }
        """)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    background-color: #e8f5e8;
                    border: 2px dashed #4CAF50;
                    border-radius: 3px;
                    color: #2c3e50;
                }
            """)
        else:
            event.ignore()
            
    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        self.setStyleSheet("""
            QLabel {
                padding: 8px;
                background-color: white;
                border: 2px dashed #ccc;
                border-radius: 3px;
                color: #666;
            }
            QLabel:hover {
                border-color: #4CAF50;
                background-color: #f0f8f0;
            }
        """)
        
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            
            # 检查是否为视频文件或文件夹
            if os.path.isdir(file_path):
                # 拖拽的是文件夹
                self.setText(file_path)
                self.setStyleSheet("""
                    QLabel {
                        padding: 8px;
                        background-color: #e8f5e8;
                        border: 2px solid #4CAF50;
                        border-radius: 3px;
                        color: #2c3e50;
                    }
                """)
                # 触发文件选择事件
                if hasattr(self, 'file_selected_callback'):
                    self.file_selected_callback(file_path)
            else:
                # 检查是否为视频文件
                video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.rmvb', '.ts'}
                if Path(file_path).suffix.lower() in video_extensions:
                    self.setText(file_path)
                    self.setStyleSheet("""
                        QLabel {
                            padding: 8px;
                            background-color: #e8f5e8;
                            border: 2px solid #4CAF50;
                            border-radius: 3px;
                            color: #2c3e50;
                        }
                    """)
                    # 触发文件选择事件
                    if hasattr(self, 'file_selected_callback'):
                        self.file_selected_callback(file_path)
                else:
                    QMessageBox.warning(None, "警告", "请拖拽视频文件或文件夹！")
                
        self.setStyleSheet("""
            QLabel {
                padding: 8px;
                background-color: white;
                border: 2px dashed #ccc;
                border-radius: 3px;
                color: #666;
            }
            QLabel:hover {
                border-color: #4CAF50;
                background-color: #f0f8f0;
            }
        """)

class ConversionWorker(QThread):
    """转换工作线程"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, video_path, output_dir, conversion_type, quality="original", ffmpeg_path="ffmpeg"):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.conversion_type = conversion_type
        self.quality = quality
        self.ffmpeg_path = ffmpeg_path
        
    def run(self):
        try:
            if self.conversion_type == "mp3":
                success = self.convert_to_mp3()
            else:
                self.finished.emit(False, "不支持的转换类型")
                return
                
            if success:
                self.finished.emit(True, "转换完成")
            else:
                self.finished.emit(False, "转换失败")
        except Exception as e:
            self.finished.emit(False, f"转换出错: {str(e)}")
    
    def convert_to_mp3(self):
        """转换为MP3"""
        try:
            video_name = Path(self.video_path).stem
            output_path = os.path.join(self.output_dir, f"{video_name}.mp3")
            
            # 构建ffmpeg命令，保持原音质
            if self.quality == "original":
                cmd = [
                    self.ffmpeg_path, "-i", self.video_path,
                    "-vn", "-acodec", "libmp3lame",
                    "-q:a", "0",  # 使用最高质量
                    "-y", output_path
                ]
            else:
                # 指定比特率
                bitrate_map = {"128k": "128k", "192k": "192k", "320k": "320k"}
                bitrate = bitrate_map.get(self.quality, "192k")
                cmd = [
                    self.ffmpeg_path, "-i", self.video_path,
                    "-vn", "-acodec", "libmp3lame",
                    "-ab", bitrate,
                    "-y", output_path
                ]
            
            self.status.emit("正在转换MP3...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.status.emit("MP3转换完成")
                return True
            else:
                self.status.emit(f"MP3转换失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.status.emit(f"MP3转换出错: {str(e)}")
            return False
    


class VideoConverterApp(QMainWindow):
    """主应用程序窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.conversion_workers = []
        self.check_ffmpeg()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("视频转音频工具 - 专业版")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QProgressBar {
                border: 2px solid #cccccc;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("🎬 视频转音频工具")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # 创建标签页
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # 转换标签页
        self.create_conversion_tab(tab_widget)
        
        # 批量处理标签页
        self.create_batch_tab(tab_widget)
        
        # 设置标签页
        self.create_settings_tab(tab_widget)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
        
    def create_conversion_tab(self, tab_widget):
        """创建转换标签页"""
        conversion_widget = QWidget()
        layout = QVBoxLayout(conversion_widget)
        
        # 文件选择组
        file_group = QGroupBox("文件选择")
        file_layout = QVBoxLayout(file_group)
        
        # 视频文件选择
        video_layout = QHBoxLayout()
        self.video_path_label = DraggableLabel("拖拽视频文件到这里，或点击按钮选择")
        self.video_path_label.file_selected_callback = self.select_video_file
        select_video_btn = QPushButton("选择视频文件")
        select_video_btn.clicked.connect(self.select_video_file)
        video_layout.addWidget(QLabel("视频文件:"))
        video_layout.addWidget(self.video_path_label, 1)
        video_layout.addWidget(select_video_btn)
        file_layout.addLayout(video_layout)
        
        # 输出目录选择
        output_layout = QHBoxLayout()
        self.output_path_label = QLabel("使用原视频目录")
        self.output_path_label.setStyleSheet("padding: 8px; background-color: white; border: 1px solid #ccc; border-radius: 3px;")
        select_output_btn = QPushButton("选择输出目录")
        select_output_btn.clicked.connect(self.select_output_directory)
        output_layout.addWidget(QLabel("输出目录:"))
        output_layout.addWidget(self.output_path_label, 1)
        output_layout.addWidget(select_output_btn)
        file_layout.addLayout(output_layout)
        
        layout.addWidget(file_group)
        
        # 转换选项组
        options_group = QGroupBox("转换选项")
        options_layout = QVBoxLayout(options_group)
        
        # MP3质量选择
        mp3_layout = QHBoxLayout()
        mp3_layout.addWidget(QLabel("MP3音质:"))
        self.mp3_quality_combo = QComboBox()
        self.mp3_quality_combo.addItems(["原视频音质", "128k", "192k", "320k"])
        mp3_layout.addWidget(self.mp3_quality_combo)
        mp3_layout.addStretch()
        options_layout.addLayout(mp3_layout)
        
        # 转换类型选择
        type_layout = QHBoxLayout()
        self.mp3_checkbox = QCheckBox("转换为MP3")
        self.mp3_checkbox.setChecked(True)
        type_layout.addWidget(self.mp3_checkbox)
        type_layout.addStretch()
        options_layout.addLayout(type_layout)
        
        layout.addWidget(options_group)
        
        # 转换按钮
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.convert_btn.setMinimumHeight(50)
        layout.addWidget(self.convert_btn)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        tab_widget.addTab(conversion_widget, "单文件转换")
        
    def create_batch_tab(self, tab_widget):
        """创建批量处理标签页"""
        batch_widget = QWidget()
        layout = QVBoxLayout(batch_widget)
        
        # 批量文件选择
        batch_group = QGroupBox("批量文件选择")
        batch_layout = QVBoxLayout(batch_group)
        
        # 目录选择
        dir_layout = QHBoxLayout()
        self.batch_dir_label = DraggableLabel("拖拽文件夹到这里，或点击按钮选择")
        self.batch_dir_label.file_selected_callback = self.select_batch_directory
        select_dir_btn = QPushButton("选择目录")
        select_dir_btn.clicked.connect(self.select_batch_directory)
        dir_layout.addWidget(QLabel("视频目录:"))
        dir_layout.addWidget(self.batch_dir_label, 1)
        dir_layout.addWidget(select_dir_btn)
        batch_layout.addLayout(dir_layout)
        
        # 文件列表
        self.file_list = QListWidget()
        batch_layout.addWidget(QLabel("视频文件列表:"))
        batch_layout.addWidget(self.file_list)
        
        layout.addWidget(batch_group)
        
        # 批量转换选项
        batch_options_group = QGroupBox("批量转换选项")
        batch_options_layout = QVBoxLayout(batch_options_group)
        
        # 转换类型
        batch_type_layout = QHBoxLayout()
        self.batch_mp3_checkbox = QCheckBox("转换为MP3")
        self.batch_mp3_checkbox.setChecked(True)
        batch_type_layout.addWidget(self.batch_mp3_checkbox)
        batch_type_layout.addStretch()
        batch_options_layout.addLayout(batch_type_layout)
        
        # MP3质量
        batch_mp3_layout = QHBoxLayout()
        batch_mp3_layout.addWidget(QLabel("MP3音质:"))
        self.batch_mp3_quality_combo = QComboBox()
        self.batch_mp3_quality_combo.addItems(["原视频音质", "128k", "192k", "320k"])
        batch_mp3_layout.addWidget(self.batch_mp3_quality_combo)
        batch_mp3_layout.addStretch()
        batch_options_layout.addLayout(batch_mp3_layout)
        
        layout.addWidget(batch_options_group)
        
        # 批量转换按钮
        self.batch_convert_btn = QPushButton("开始批量转换")
        self.batch_convert_btn.clicked.connect(self.start_batch_conversion)
        self.batch_convert_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.batch_convert_btn.setMinimumHeight(50)
        layout.addWidget(self.batch_convert_btn)
        
        # 批量进度条
        self.batch_progress_bar = QProgressBar()
        self.batch_progress_bar.setVisible(False)
        layout.addWidget(self.batch_progress_bar)
        
        # 批量状态显示
        self.batch_status_text = QTextEdit()
        self.batch_status_text.setMaximumHeight(150)
        self.batch_status_text.setReadOnly(True)
        layout.addWidget(self.batch_status_text)
        
        tab_widget.addTab(batch_widget, "批量转换")
        
    def create_settings_tab(self, tab_widget):
        """创建设置标签页"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        
        # FFmpeg状态
        ffmpeg_group = QGroupBox("FFmpeg状态")
        ffmpeg_layout = QVBoxLayout(ffmpeg_group)
        
        self.ffmpeg_status_label = QLabel("检查中...")
        self.ffmpeg_status_label.setStyleSheet("padding: 10px; font-weight: bold;")
        ffmpeg_layout.addWidget(self.ffmpeg_status_label)
        
        check_ffmpeg_btn = QPushButton("重新检查FFmpeg")
        check_ffmpeg_btn.clicked.connect(self.check_ffmpeg)
        ffmpeg_layout.addWidget(check_ffmpeg_btn)
        
        layout.addWidget(ffmpeg_group)
        
        # 关于信息
        about_group = QGroupBox("关于")
        about_layout = QVBoxLayout(about_group)
        
        about_text = QLabel("""
        <h3>视频转音频工具 v1.0</h3>
        <p>功能特性：</p>
        <ul>
            <li>🎵 视频转MP3（保持原音质）</li>
            <li>📁 批量处理支持</li>
            <li>🎨 精美现代化界面</li>
        </ul>
        <p>技术支持：基于FFmpeg</p>
        """)
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)
        
        layout.addWidget(about_group)
        
        layout.addStretch()
        
        tab_widget.addTab(settings_widget, "设置")
        
    def select_video_file(self, file_path=None):
        """选择视频文件"""
        if file_path is None:
            # 通过文件对话框选择
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择视频文件", "",
                "视频文件 (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v *.3gp *.rmvb *.ts)"
            )
        
        if file_path:
            self.video_path_label.setText(file_path)
            # 自动设置输出目录为原视频目录
            self.output_path_label.setText(os.path.dirname(file_path))
            
    def select_output_directory(self):
        """选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_path_label.setText(dir_path)
            
    def select_batch_directory(self, dir_path=None):
        """选择批量处理目录"""
        if dir_path is None:
            # 通过文件对话框选择
            dir_path = QFileDialog.getExistingDirectory(self, "选择视频目录")
        
        if dir_path:
            # 检查是否为目录
            if os.path.isdir(dir_path):
                self.batch_dir_label.setText(dir_path)
                self.load_video_files(dir_path)
            else:
                QMessageBox.warning(self, "警告", "请选择文件夹！")
            
    def load_video_files(self, directory):
        """加载目录中的视频文件"""
        self.file_list.clear()
        video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.rmvb', '.ts'}
        
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix.lower() in video_extensions:
                item = QListWidgetItem(str(file_path))
                self.file_list.addItem(item)
                
        self.batch_status_text.append(f"找到 {self.file_list.count()} 个视频文件")
        
    def start_conversion(self):
        """开始转换"""
        if not hasattr(self, 'video_path_label') or not self.video_path_label.text() or "拖拽视频文件到这里" in self.video_path_label.text():
            QMessageBox.warning(self, "警告", "请先选择视频文件")
            return
            
        video_path = self.video_path_label.text()
        output_dir = self.output_path_label.text() if self.output_path_label.text() != "使用原视频目录" else os.path.dirname(video_path)
        
        # 检查转换类型
        conversion_types = []
        if self.mp3_checkbox.isChecked():
            conversion_types.append("mp3")
            
        if not conversion_types:
            QMessageBox.warning(self, "警告", "请选择转换为MP3")
            return
            
        # 获取MP3质量
        quality = self.mp3_quality_combo.currentText()
        if quality == "原视频音质":
            quality = "original"
        else:
            quality = quality.replace("k", "k")
            
        # 开始转换
        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(conversion_types))
        self.progress_bar.setValue(0)
        
        self.status_text.clear()
        self.status_text.append(f"开始转换: {os.path.basename(video_path)}")
        
        # 创建转换线程
        for i, conv_type in enumerate(conversion_types):
            worker = ConversionWorker(video_path, output_dir, conv_type, quality, 
                                    getattr(self, 'ffmpeg_path', 'ffmpeg'))
            worker.progress.connect(lambda val, idx=i: self.progress_bar.setValue(idx + 1))
            worker.status.connect(self.status_text.append)
            worker.finished.connect(lambda success, msg, idx=i: self.on_conversion_finished(success, msg, idx))
            
            self.conversion_workers.append(worker)
            worker.start()
            
    def start_batch_conversion(self):
        """开始批量转换"""
        if self.file_list.count() == 0 or "拖拽文件夹到这里" in self.batch_dir_label.text():
            QMessageBox.warning(self, "警告", "请先选择包含视频文件的目录")
            return
            
        # 检查转换类型
        conversion_types = []
        if self.batch_mp3_checkbox.isChecked():
            conversion_types.append("mp3")
            
        if not conversion_types:
            QMessageBox.warning(self, "警告", "请选择转换为MP3")
            return
            
        # 获取MP3质量
        quality = self.batch_mp3_quality_combo.currentText()
        if quality == "原视频音质":
            quality = "original"
        else:
            quality = quality.replace("k", "k")
            
        # 开始批量转换
        self.batch_convert_btn.setEnabled(False)
        self.batch_progress_bar.setVisible(True)
        self.batch_progress_bar.setMaximum(self.file_list.count() * len(conversion_types))
        self.batch_progress_bar.setValue(0)
        
        self.batch_status_text.clear()
        self.batch_status_text.append("开始批量转换...")
        
        # 创建批量转换线程
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            video_path = item.text()
            output_dir = os.path.dirname(video_path)
            
            for j, conv_type in enumerate(conversion_types):
                worker = ConversionWorker(video_path, output_dir, conv_type, quality,
                                        getattr(self, 'ffmpeg_path', 'ffmpeg'))
                worker.progress.connect(lambda val, idx=i*len(conversion_types)+j: self.batch_progress_bar.setValue(idx + 1))
                worker.status.connect(self.batch_status_text.append)
                worker.finished.connect(lambda success, msg, idx=i*len(conversion_types)+j: self.on_batch_conversion_finished(success, msg, idx))
                
                self.conversion_workers.append(worker)
                worker.start()
                
    def on_conversion_finished(self, success, message, index):
        """单个转换完成回调"""
        self.status_text.append(message)
        if index == len(self.conversion_workers) - 1:
            self.convert_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
            if success:
                QMessageBox.information(self, "完成", "转换完成！")
            else:
                QMessageBox.warning(self, "警告", "部分转换失败，请查看日志")
                
    def on_batch_conversion_finished(self, success, message, index):
        """批量转换完成回调"""
        self.batch_status_text.append(message)
        if index == self.batch_progress_bar.maximum() - 1:
            self.batch_convert_btn.setEnabled(True)
            self.batch_progress_bar.setVisible(False)
            if success:
                QMessageBox.information(self, "完成", "批量转换完成！")
            else:
                QMessageBox.warning(self, "警告", "部分转换失败，请查看日志")
                
    def check_ffmpeg(self):
        """检查FFmpeg是否可用"""
        # 首先尝试检测本地项目目录中的FFmpeg
        local_ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                        "ffmpeg-7.1-essentials_build", "bin", "ffmpeg.exe")
        
        if os.path.exists(local_ffmpeg_path):
            # 使用本地FFmpeg
            self.ffmpeg_path = local_ffmpeg_path
            self.ffprobe_path = os.path.join(os.path.dirname(local_ffmpeg_path), "ffprobe.exe")
            self.ffplay_path = os.path.join(os.path.dirname(local_ffmpeg_path), "ffplay.exe")
            
            try:
                result = subprocess.run([local_ffmpeg_path, "-version"], capture_output=True, text=True)
                if result.returncode == 0:
                    self.ffmpeg_status_label.setText("✅ 本地FFmpeg 可用")
                    self.ffmpeg_status_label.setStyleSheet("padding: 10px; font-weight: bold; color: green;")
                    self.statusBar().showMessage("本地FFmpeg 检查通过")
                    return
            except Exception:
                pass
        
        # 如果本地FFmpeg不可用，尝试系统PATH中的FFmpeg
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.ffmpeg_path = "ffmpeg"
                self.ffprobe_path = "ffprobe"
                self.ffplay_path = "ffplay"
                self.ffmpeg_status_label.setText("✅ 系统FFmpeg 可用")
                self.ffmpeg_status_label.setStyleSheet("padding: 10px; font-weight: bold; color: green;")
                self.statusBar().showMessage("系统FFmpeg 检查通过")
            else:
                self.ffmpeg_status_label.setText("❌ FFmpeg 不可用")
                self.ffmpeg_status_label.setStyleSheet("padding: 10px; font-weight: bold; color: red;")
                self.statusBar().showMessage("FFmpeg 检查失败")
        except FileNotFoundError:
            self.ffmpeg_status_label.setText("❌ FFmpeg 未安装")
            self.ffmpeg_status_label.setStyleSheet("padding: 10px; font-weight: bold; color: red;")
            self.statusBar().showMessage("FFmpeg 未安装，请先安装 FFmpeg")
            
    def closeEvent(self, event):
        """关闭事件"""
        # 停止所有转换线程
        for worker in self.conversion_workers:
            if worker.isRunning():
                worker.terminate()
                worker.wait()
        event.accept()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("视频转音频工具")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("AI Assistant")
    
    # 创建主窗口
    window = VideoConverterApp()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

