from qgis.core import QgsProcessingAlgorithm, QgsProcessingParameterString, QgsProcessingParameterVectorLayer
import subprocess

class OpenExeAlgorithm(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        # Define parameters
        self.addParameter(QgsProcessingParameterVectorLayer('input_layer', 'Input Vector Layer'))
        self.addParameter(QgsProcessingParameterString('exe_path', 'Executable Path', defaultValue=r'E:\Python\QGIS_BGS_BEDROCK\venv\dist\bgs_bedrock.exe'))
        self.addParameter(QgsProcessingParameterString('output_folder', 'Output Folder', defaultValue=r'Enter an output folder'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Get the value of the 'exe_path' parameter
        exe_path = self.parameterAsString(parameters, 'exe_path', context)

        # Get the input vector layer
        input_layer = self.parameterAsVectorLayer(parameters, 'input_layer', context)

        # Get the output folder
        output_folder = self.parameterAsString(parameters, 'output_folder', context)

        # Get the extent of the vector layer
        extent = input_layer.extent()
        x1, y1, x2, y2 = extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()

        # Adjust the subprocess command
        command = [exe_path, str(x1), str(y1), str(x2), str(y2), '-o', output_folder]
        print("Subprocess command:", " ".join(command))

        # Use subprocess to open the executable with parameters
        subprocess.Popen(command, shell=True)

        return {}

    def name(self):
        return 'BGS Bedrock Download'

    def displayName(self):
        return 'BGS Bedrock Download'

    def group(self):
        return 'Site Investigation'

    def groupId(self):
        return 'siteinvestigation'

    def createInstance(self):
        return OpenExeAlgorithm()
