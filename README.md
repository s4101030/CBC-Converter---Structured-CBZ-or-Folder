# CBC Converter - Structured CBZ or Folder
When doing some archiving I accidentally downloaded stuff in the wrong format/structure for automatic chapter detection, my wifi isn't good enough for redownloading so I made this tool.

### Usage:  
`python cbz2cbc 'fileorfolder' [-delete/-omove] [-nmove]`  
`-delete` - Delete original cbz file or folder when done  
`-omove` - Move original cbz file or folder when done  
`-nmove` - Move new cbc file when done  
`-h` - Show this guide

### Format must be:  
`file.cbz/chapterfolder/images`  
OR  
`folder/chapterfolder/images`  
The key requirement is that the images are in FOLDERS for each chapter, the names of those folders are treated as the names of the chapters for the comics.txt

### Notes:  
This should automatically detect cbz file vs folder, but it's not ideal  
This was slapped together and is held by duct-tape, I am by no means good at coding, I just enjoy it  
This was made for me because I couldn't find a tool to do the job, this means it only does the stuff I wanted it to  

I hope this may be of use to someone else who is in the same situation I was
