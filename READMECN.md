# Aninamer

<center>
<img src="./image/icon.svg" width = "512" width = "512"  alt="Aninamer" />
</center>

### 一个自动重命名软件，可以优化与 RSS 动画订阅和如 emby 等刮削软件的配合。

<a href="README.md">English README file

## 功能

![function](./image/function.png)

![function](./image/function2.png)

## 如何使用

### Windows

因为 Docker for Windows 对 watchdog 的支持不好，我并不推荐在 Windows 使用 docker 版本。

1. 下载并解压最新版本的 Release 到你想要的文件夹

2. 最好确保你订阅的剧集有一个基本的分类。包含像这样的名称和季数。（与 Aninamer 运行无关，只是为了方便刮削 Aninamer 获取剧集元数据与季元数据）

   ![basic classification](./image/basic_classification.png)

3. 运行 Aninamer，Aninamer 会生成一些配置文件。Aninamer 默认监控 exe 目录下的一个 video 文件夹，请在配置文件里输入你要检测的目录，比如上图的 `D:\download\anime`。你可以直接编辑 conf 文件夹下的 `path.json`，或者在打开 Aninamer 之后，可以右键托盘图标来打开配置文件。修改完毕后记得重启程序。

4. 如果目录没有问题，现在应已经重命名完毕了，你可以刷新你的刮削 Aninamer，获取每一集的元数据。

5. 托盘图标中可以手动重命名Rename或是恢复Recover原有文件

6. conf 文件夹中可能会出现三个文件，`path.json` 负责读取监测目录，可以是多个目录，加上引号`""`后用逗号`,`隔开。`directory_tree.json` 是监控文件夹的树状结构信息，所有文件和目录都包含一个布尔值，负责控制文件或目录下是否进行重命名，可以手动修改为`true`或者`false`，对于文件还包含两个文件名，第一个是原始文件名，第二个是重命名后的文件名，一般情况下不需要修改，如果有需要可以直接更改。`deleted_tree.json` 是过去由于监控目录更改或是文件变动而丢失的`directory_tree.json` 中的信息，根据信息重要程度自动删除（保留 7 天或 30 天），**不建议**手动修改或删除，除非你认识到这会带来不可逆的数据损失并且执意删除。

7. 如果你愿意，你也可以在`startup`文件夹中添加一个快捷方式，让 Aninamer 在开机时自动运行。按`win`+`R`，输入`shell:startup`，打开`startup`文件夹。

### Docker

1. 最好确保你订阅的剧集有一个基本的分类。包含像这样的名称和季数。（与 Aninamer 运行无关，只是为了方便刮削软件获取剧集元数据与季元数据）

   ![basic classification](./image/basic_classification.png)

2. 拉取 mistarille/aninamer:latest，映射你的视频文件夹到`/app/video`，为了避免删除容器后配置文件失效，映射一个 conf 文件夹到`/app/conf`，运行容器。

```bash
   docker run --name aninamer --restart=always -v /path/to/your/video/folder:/app/video -v  /path/to/your/conf/folder:/app/conf mistarille/aninamer:latest
```

3. 如果你的目录没有映射到`/app/video`，或者你映射了多个目录到容器中，你需要手动在配置文件里输入你要检测的目录。你可以直接编辑 conf 文件夹下的 `path.json`。

4. 如果目录没有问题，现在应已经重命名完毕了，你可以刷新你的刮削 Aninamer，获取每一集的元数据。

5. 可以在docker终端中执行命令

   ```bash
   aninamer rename
   ```

    或者

   ```bash
   aninamer recover
   ```

   来进行手动重命名或恢复

6. conf 文件夹中可能会出现三个文件，`path.json` 负责读取监测目录，可以是多个目录，加上引号`""`后用逗号`,`隔开。`directory_tree.json` 是监控文件夹的树状结构信息，所有文件和目录都包含一个布尔值，负责控制文件或目录下是否进行重命名，可以手动修改为`true`或者`false`，对于文件还包含两个文件名，第一个是原始文件名，第二个是重命名后的文件名，一般情况下不需要修改，如果有需要可以直接更改。`deleted_tree.json` 是过去由于监控目录更改或是文件变动而丢失的`directory_tree.json` 中的信息，根据信息重要程度自动删除（保留 7 天或 30 天），**不建议**手动修改或删除，除非你认识到这会带来不可逆的数据损失并且执意删除。

## 卸载

直接删除即可，如果希望恢复原来的文件名，记得卸载前进行一次恢复
