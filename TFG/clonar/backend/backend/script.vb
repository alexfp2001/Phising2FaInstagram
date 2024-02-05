Imports System.Diagnostics
Imports System.IO

Public Class Form1
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        ' Iniciar un proceso de la línea de comandos
        Dim cmdProcess As New Process()

        ' Configurar el proceso
        Dim cmdStartInfo As New ProcessStartInfo()
        cmdStartInfo.FileName = "cmd.exe" ' Nombre del ejecutable de la línea de comandos
        cmdStartInfo.RedirectStandardInput = True ' Redirigir la entrada estándar
        cmdStartInfo.RedirectStandardOutput = True ' Redirigir la salida estándar
        cmdStartInfo.UseShellExecute = False ' No utilizar el shell para iniciar el proceso
        cmdStartInfo.CreateNoWindow = True ' No crear una ventana para el proceso

        ' Asignar la configuración al proceso
        cmdProcess.StartInfo = cmdStartInfo

        ' Iniciar el proceso
        cmdProcess.Start()

        ' Obtener el flujo de entrada estándar
        Dim cmdStreamWriter As StreamWriter = cmdProcess.StandardInput

        ' Escribir en la ventana de comandos
        cmdStreamWriter.WriteLine("echo Hola desde Visual Basic")
        cmdStreamWriter.WriteLine("pause") ' Pausar la ventana de comandos

        ' Cerrar el flujo de escritura
        cmdStreamWriter.Close()
    End Sub
End Class
