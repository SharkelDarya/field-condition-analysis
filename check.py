import rasterio

# Пути к файлам
tiff_b08_file = 'raster_data/B08.tiff'  # TIFF для инфракрасного канала
tiff_b04_file = 'raster_data/B04.tiff'  # TIFF для красного канала

# Функция для загрузки и проверки метаданных растрового файла
def check_raster_metadata(tiff_path):
    with rasterio.open(tiff_path) as src:
        print(f"Метаданные для файла {tiff_path}:")
        print(f"Размер изображения: {src.shape}")
        print(f"Границы (bounds): {src.bounds}")
        print(f"CRS (система координат): {src.crs}")
        print(f"Данные о трансформации (transform): {src.transform}")
        print("="*50)

# Проверяем метаданные для обоих растров
check_raster_metadata(tiff_b08_file)
check_raster_metadata(tiff_b04_file)
