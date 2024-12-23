# Aninamer

<img src="./image/icon.svg" width="512" alt="Aninamer" align="center"/>


### An automatic renaming software that can optimize the collaboration with RSS anime subscriptions and scraping software such as emby.

<a href="READMECN.md">Chinese README file

## Features

![function](./image/function.png)

![function](./image/function2.png)

## How to Use

### Windows

I do not recommend using the Docker version on Windows due to poor support for watchdog in Docker for Windows.

1. Download and unzip the latest version of the Release to the folder you want.

2. It is best to ensure that the series you subscribe to has a basic classification, including names and seasons like these. (This is not related to Aninamer's operation but is for convenience in scraping Aninamer to obtain series metadata and season metadata.)

   ![basic classification](./image/basic_classification.png)

3. Run Aninamer, which will generate some configuration files. Aninamer by default monitors a video folder under the exe directory. Please enter the directory you want to monitor in the configuration file, such as `D:\download\anime` shown above. You can directly edit the `path.json` in the conf folder, or right-click the tray icon to open the configuration file after opening Aninamer. Remember to restart the program after modification.

4. If there is no problem with the directory, it should have been renamed now. You can refresh your scraper to obtain metadata for each episode.

5. In the tray icon, you can manually rename or recover the original files.

6. The conf folder may have three files. `path.json` is responsible for reading the monitored directories, which can be multiple directories separated by commas `,` and enclosed in quotes `""`. `directory_tree.json`is the tree structure information of the monitored folder, where all files and directories have a boolean value that controls whether renaming occurs. You can manually change it to`true`or`false`. For files, it also includes two filenames, the original and the renamed ones. Generally, you do not need to modify this, but if needed, you can directly change it. `deleted_tree.json`contains information from`directory_tree.json` that was lost due to directory changes or file movements. This data is automatically deleted based on its importance (retained for 7 or 30 days). Manual modification or deletion **is not recommended** unless you recognize the irreversible data loss and insist on deleting it.

7. If you wish, you can also add a shortcut to the `startup` folder to have Aninamer run automatically at startup. Press `win`+`R`, enter `shell:startup`, and open the `startup` folder.

### Docker

1. It is best to ensure that the series you subscribe to has a basic classification, including names and seasons like these. (This is not related to Aninamer's operation but is for convenience in scraping software to obtain series metadata and season metadata.)

   ![basic classification](./image/basic_classification.png)

2. Pull mistarille/aninamer:latest, map your video folder to `/app/video`, and to avoid configuration file loss after deleting the container, map a conf folder to `/app/conf`, and run the container.

```bash
   docker run --name aninamer --restart=always -v /path/to/your/video/folder:/app/video -v  /path/to/your/conf/folder:/app/conf mistarille/aninamer:latest
```

3. If your directory is not mapped to `/app/video` or if you have mapped multiple directories to the container, you need to manually enter the directories to be monitored in the configuration file. You can directly edit the `path.json` in the conf folder.

4. If there is no problem with the directory, it should have been renamed now. You can refresh your scraper to obtain metadata for each episode.

5. You can execute commands in the docker terminal

   ```bash
   aninamer rename
   ```

   or

   ```bash
   aninamer recover
   ```

   to manually rename or recover.

6. The conf folder may have three files. `path.json` is responsible for reading the monitored directories, which can be multiple directories separated by commas `,` and enclosed in quotes `""`. `directory_tree.json`is the tree structure information of the monitored folder, where all files and directories have a boolean value that controls whether renaming occurs. You can manually change it to`true`or`false`. For files, it also includes two filenames, the original and the renamed ones. Generally, you do not need to modify this, but if needed, you can directly change it. `deleted_tree.json`contains information from`directory_tree.json` that was lost due to directory changes or file movements. This data is automatically deleted based on its importance (retained for 7 or 30 days). Manual modification or deletion **is not recommended** unless you recognize the irreversible data loss and insist on deleting it.

## Uninstall

Just delete it. If you want to restore the original filenames, remember to perform a recovery before uninstalling.
