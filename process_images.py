import cv2
import numpy as np
import os

def get_blue_box_coordinates(reference_image_path):
    """从参考图片中获取蓝色框的坐标
    
    参数:
        reference_image_path: 参考图片的路径
        
    返回:
        蓝色框的坐标 (x, y, width, height)
    """
    img = cv2.imdecode(np.fromfile(reference_image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise Exception(f"无法读取参考图片: {reference_image_path}")
        
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 定义蓝色的HSV范围
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    # 创建蓝色区域的掩码
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # 形态学操作
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        raise Exception("在参考图片中未找到蓝色框")
    
    # 获取最大轮廓（蓝色框）
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    
    return x, y, w, h

def process_image(input_path, output_path, box_coords):
    """处理单个图片：直接裁剪保存
    
    参数:
        input_path: 输入图片的路径
        output_path: 输出裁剪后图片的路径
        box_coords: 裁剪框的坐标 (x, y, width, height)
        
    返回:
        成功处理返回True，否则返回False
    """
    try:
        # 使用imdecode读取图片以支持中文路径
        img = cv2.imdecode(np.fromfile(input_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            print(f"无法读取图片: {input_path}")
            return False
        
        x, y, w, h = box_coords
        
        # 确保坐标不会超出图片边界
        y = max(0, min(y, img.shape[0]))
        h = min(h, img.shape[0] - y)
        x = max(0, min(x, img.shape[1]))
        w = min(w, img.shape[1] - x)
        
        # 裁剪图片
        cropped = img[y:y+h, x:x+w]
        
        # 使用imencode和tofile来保存带中文路径的图片
        _, img_encoded = cv2.imencode('.png', cropped)
        img_encoded.tofile(output_path)
        return True
    except Exception as e:
        print(f"处理图片时出错: {str(e)}")
        return False

def main():
    reference_path = r"E:\CUT-7\11map_1500.png"
    input_dir = r"E:\CUT-7\13\公元前"
    output_dir = r"E:\CUT-7\0001\00001_crop0"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 获取参考图片中蓝色框的坐标
        print("正在分析参考图片中的蓝色框位置...")
        box_coords = get_blue_box_coordinates(reference_path)
        print(f"找到蓝色框坐标: x={box_coords[0]}, y={box_coords[1]}, width={box_coords[2]}, height={box_coords[3]}")
        
        # 处理文件夹中的所有PNG图片
        total_files = len([f for f in os.listdir(input_dir) if f.lower().endswith('.png')])
        processed_files = 0
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith('.png'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                print(f"处理图片 ({processed_files + 1}/{total_files}): {filename}")
                try:
                    success = process_image(input_path, output_path, box_coords)
                    if success:
                        processed_files += 1
                        print(f"已将裁剪后的图片保存到: {output_path}")
                except Exception as e:
                    print(f"处理 {filename} 时出错: {str(e)}")
        
        print(f"\n处理完成！成功处理 {processed_files}/{total_files} 个文件")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()