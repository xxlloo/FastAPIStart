import random
import string
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


class CaptchaUtils:
    @staticmethod
    def generate_random_code(length: int = 6) -> str:
        """
        生成一个随机数字验证码
        :param length: 验证码的长度，默认为 6
        :return: 随机生成的验证码字符串
        """
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def generate_image_captcha(
        code: str, width: int = 160, height: int = 60
    ) -> BytesIO:
        """
        生成一个图片验证码
        :param code: 验证码的文本内容（例如：6位数字）
        :param width: 图片宽度
        :param height: 图片高度
        :return: 包含验证码图像的 BytesIO 对象
        """
        # 创建空白图片
        image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()  # 如果没有 arial 字体，则使用默认字体

        bbox = draw.textbbox((0, 0), code, font=font)
        text_width = (
            bbox[2] - bbox[0]
        )  # bbox[2] 是右下角 x 坐标，bbox[0] 是左上角 x 坐标
        text_height = (
            bbox[3] - bbox[1]
        )  # bbox[3] 是右下角 y 坐标，bbox[1] 是左上角 y 坐标

        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2

        draw.text((text_x, text_y), code, font=font, fill=(0, 0, 0))

        for _ in range(5):
            start_x = random.randint(0, width)
            start_y = random.randint(0, height)
            end_x = random.randint(0, width)
            end_y = random.randint(0, height)
            draw.line((start_x, start_y, end_x, end_y), fill=(0, 0, 0), width=2)

        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill=(0, 0, 0))

        img_io = BytesIO()
        image.save(img_io, "PNG")
        img_io.seek(0)  # 重置文件指针
        return img_io


# 使用示例：
# captcha = CaptchaUtils.generate_random_code(6)  # 生成 6 位纯数字验证码
# print(captcha)
# image = CaptchaUtils.generate_image_captcha(captcha)  # 生成图片验证码
