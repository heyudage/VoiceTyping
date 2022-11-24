## 语音输入（VoiceTyping）
通过语音（说话）即可完成实时文本输入。通过[PaddleSpeech项目二次开发](https://github.com/PaddlePaddle/PaddleNLP) 完成，支持离线脱网环境部署，支持GPU推理，目前客户端仅支持Windows。

### 一、环境部署安装
#### 1.安装PaddleSpeech
安装最新版PaddleSpeech，[安装教程](https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/get_started/installation.rst) 。
#### 2.安装相关模块
安装requirements.txt中的模块

### 一、服务端
#### 启动命令
`python streaming_asr_server.py --config_file .\conf\ws_conformer_wenetspeech_application.yaml`

#### 配置文件config_file
配置文件（conf下，具体可参考PaddleSpeech文档）可选：
+ ws_conformer_application.yaml
+ ws_conformer_wenetspeech_application.yaml
+ ws_conformer_wenetspeech_application_faster.yaml
+ ws_ds2_application.yaml

### 二、客户端
#### 启动命令
`python main.py`
#### 打包二进制文件
入口文件main.py，根据需要可改变命令。
`pyinstaller -F -w main.py`

### TODO