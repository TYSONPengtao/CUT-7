# 图片裁剪工具

这是一个用于批量处理图片的 Python 工具，可以根据参考图片中的蓝色框区域裁剪其他图片。

## 功能特点

- 自动检测参考图片中的蓝色框区域
- 支持批量处理图片
- 支持中文路径
- 自动调整裁剪区域以避免越界
- 保持原始图片质量

## 环境要求

- Python 3.6+
- OpenCV (cv2)
- NumPy

## 安装依赖

```bash
pip install opencv-python numpy
```

## 使用方法

1. 准备参考图片（含有蓝色框的图片）
2. 修改 `process_images.py` 中的路径配置：
   - reference_path: 参考图片路径
   - input_dir: 待处理图片所在文件夹
   - output_dir: 处理后图片保存路径
3. 运行脚本：
   ```bash
   python process_images.py
   ```

## 代码结构

- `process_images.py`: 主程序
  - `get_blue_box_coordinates()`: 获取参考图片中蓝色框坐标
  - `process_image()`: 处理单个图片
  - `main()`: 程序入口
