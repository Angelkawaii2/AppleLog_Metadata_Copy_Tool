# BlackMagic Apple Log Metadata Copy Tool

This tool is designed to copy metadata from original Apple Log video files to your edited videos.

By doing so, it ensures that when you transfer your edited videos back to your iPhone, they retain all original details
and appear just like the originals in your Photos app.

在对 Apple Log 视频进行处理时，有时您可能希望将其重新导入回 iOS 设备中观看。 然而，目前的视频编辑软件在渲染视频时往往会丢失原始的拍摄信息，导致您在将视频重新导入
iOS 设备后，需要重新添加位置信息、编辑拍摄时间等，这一过程非常不便利。

本工具通过将原始 Apple Log 视频中的 metadata 拷贝到目标视频中，能够帮助您解决这个问题。使用这个脚本后，您处理过的视频重新导入
iOS 设备时，可以在相册 APP 中正确显示视频的元数据信息，如镜头、GPS 位置等。

## 准备环境 | Prerequisites

1. Python 3.12+ (更低版本未测试)
2. 原始的 ProRes(Apple Log) 视频文件
3. 需要导入回iOS设备的视频文件（例如已经调色的视频）

## 使用方法 | Usage

```bash
main.py <prores_path> <rendered_path> <output_path>
```

- prores_path: 原始的Apple Log文件目录
- rendered_path: 待处理的目标文件
- output_path: 输出目录

注意: 对于待处理的目标文件，文件名中需要完全包含原始 Apple log 视频文件的文件名称，例如原始的文件名为``A000_114514.MOV``
，那么目标的文件名可以是``A000_114514.MOV.RENDERED.mp4``

Note: For the target files to be processed, the filename must include the full name of the original Apple Log video
file. For example, if the original file is named A000_114514.MOV, then the target file name could be
A000_114514.MOV.RENDERED.mp4.

## 开源许可证 | License

MIT

## 致谢 | Acknowledgments

wywh: [macOS Photos app ignores GPS Data on mp4 file import](https://exiftool.org/forum/index.php?topic=15418.msg82847#msg82847)
