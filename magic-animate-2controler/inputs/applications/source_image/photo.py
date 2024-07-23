from PIL import Image

image = Image.open("girl.png")
aspect_ratio = image.width / image.height

if aspect_ratio > 1:
    new_width = 512
    new_height = int(new_width / aspect_ratio)
else:
    new_height = 512
    new_width = int(new_height * aspect_ratio)

resized_image = image.resize((new_width, new_height))

padded_image = Image.new("RGB", (512, 512), resized_image.getpixel((3, 3)))
# print(image.getpixel((50, 50)))
paste_position = ((512 - new_width) // 2, (512 - new_height) // 2)
padded_image.paste(resized_image, paste_position)

padded_image.save("girl.png")

# image = Image.open("jyx3.png")
# image = image.resize((512, 512))
# image = image.convert("RGB")
# image.save("jyx3.png")

# image = Image.open("jyx4.png")
# image = image.resize((512, 512))
# image = image.convert("RGB")
# image.save("jyx4.png")

# image = Image.open("tx.jpg")
# image = image.resize((512, 512))
# image = image.convert("RGB")
# image.save("tx.png")


