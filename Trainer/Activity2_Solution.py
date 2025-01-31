class Product:
    def __init__(self, product_category, product_type):
        """
        Initialize a Product object.

        Args:
            product_category (str): Category of the product (e.g., "Audio Devices").
            product_type (str): Specific type of product (e.g., "Speaker").
        """
        self.product_category = product_category
        self.product_type = product_type

    def product_details(self):
        """
        Get the details of the product.

        Returns:
            str: Product details as a string.
        """
        return f"Category: {self.product_category}, Type: {self.product_type}"

    def description(self):
        """
        A placeholder method for product-specific descriptions.

        Returns:
            str: Placeholder text.
        """
        return "This is a generic product."

class AudioDevice(Product):
    def __init__(self, product_type, power_consumption):
        """
        Initialize an Audio Device object.

        Args:
            product_type (str): Specific type of audio device (e.g., "Speaker").
            power_consumption (int): Power consumption in watts.
        """
        super().__init__("Audio Devices", product_type)
        self.power_consumption = power_consumption

    def description(self):
        """
        Provides a specific description for audio devices.

        Returns:
            str: Description of the audio device.
        """
        return f"{self.product_type} is an audio device consuming {self.power_consumption} watts of power."

    def adjust_volume(self, level):
        """
        Simulate adjusting the volume of the device.

        Args:
            level (int): Volume level to adjust to.

        Returns:
            str: Confirmation of volume adjustment.
        """
        return f"Volume of the {self.product_type} adjusted to level {level}."

class VideoDevice(Product):
    def __init__(self, product_type, resolution):
        """
        Initialize a Video Device object.

        Args:
            product_type (str): Specific type of video device (e.g., "Camera").
            resolution (str): Resolution of the video device (e.g., "4K").
        """
        super().__init__("Video Devices", product_type)
        self.resolution = resolution

    def description(self):
        """
        Provides a specific description for video devices.

        Returns:
            str: Description of the video device.
        """
        return f"{self.product_type} is a video device with {self.resolution} resolution."

    def capture(self):
        """
        Simulate capturing a video or photo.

        Returns:
            str: Confirmation of capture.
        """
        return f"{self.product_type} has captured a new video/photo at {self.resolution} resolution."

if __name__ == "__main__":
    # Create instances of Audio Devices
    speaker = AudioDevice("Speaker", 50)
    microphone = AudioDevice("Microphone", 10)

    # Create an instance of Video Device
    camera = VideoDevice("Camera", "4K")

    # Showcase Polymorphism: Using the `description` method
    devices = [speaker, microphone, camera]
    for device in devices:
        print(device.description())

    print("\n--- Unique Methods ---")
    # Call unique methods of child classes
    print(speaker.adjust_volume(5))
    print(camera.capture())
