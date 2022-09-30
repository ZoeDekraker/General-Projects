Add-Type -assemblyname system.speech
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Convert text in box to speech
function Read-Aloud()
 {
    $data = $textBox1.Text
    $speaker = [System.Speech.Synthesis.SpeechSynthesizer]::new()
    $speaker.SelectVoice("Microsoft Zira Desktop")
    $speaker.Speak($data)
    
}

# Save text in box to file
function Save-File()
{
    [System.Reflection.Assembly]::LoadWithPartialName("System.windows.forms") | Out-Null

    $SaveFileDialog = New-Object System.Windows.Forms.SaveFileDialog
    $SaveFileDialog.initialDirectory = $initialDirectory
    $SaveFileDialog.filter = "Text Document (*.txt)| *.txt"
    $SaveFileDialog.ShowDialog() |  Out-Null
    $addy = $SaveFileDialog.FileName
    $textBox1.Text | Out-File $addy

}


#------------------GUI----------------------#


# New Windows Form
$form = New-Object System.Windows.Forms.Form
$form.Text = 'Read Aloud with PowerShell' 
$form.Size = New-Object System.Drawing.Size(540, 570) #  w x h
$form.StartPosition = 'CenterScreen' 
$form.Topmost = $true

# read aloud button
$readButton = New-Object System.Windows.Forms.Button
$readButton.Location = New-Object System.Drawing.Point(120,25) 
$readButton.Size = New-Object System.Drawing.Size(90,75)
$readButton.Text = 'Read Aloud'
$form.Controls.Add($readButton)
$readButton.Add_Click({Read-Aloud})

# save text button
$saveButton = New-Object System.Windows.Forms.Button
$saveButton.Location = New-Object System.Drawing.Point(317.5,25) 
$saveButton.Size = New-Object System.Drawing.Size(90,75)
$saveButton.Text = 'Save Text'
$form.Controls.Add($saveButton)
$saveButton.Add_Click({Save-File})

# text box
$textBox1 = New-Object System.Windows.Forms.TextBox
$textBox1.Location = New-Object System.Drawing.Point(30,130)
$textBox1.Size = New-Object System.Drawing.Size(460,300)
$textBox1.Multiline = $true
$textBox1.PlaceholderText = 'Enter your text here'
$textBox1.ScrollBars = "Vertical"
$textBox1.AcceptsReturn = $true
$textBox1.AcceptsTab = $true
$textBox1.WordWrap = $true
$form.Controls.Add($textBox1)

# cancel button
$cancelButton = New-Object System.Windows.Forms.Button
$cancelButton.Location = New-Object System.Drawing.Point(405,460) 
$cancelButton.Size = New-Object System.Drawing.Size(75,45)
$cancelButton.Text = 'Cancel'
$form.Controls.Add($cancelButton)
$cancelButton.DialogResult = 'Ok' #close form


# show form
$form.ShowDialog()
