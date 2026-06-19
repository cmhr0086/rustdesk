# 自定义 RustDesk 客户端维护说明

本仓库的自定义标签构建仅发布以下产物：

- Windows x64 Flutter 自解压安装版（`*-x86_64-flutter.exe`）
- Windows x64 Flutter MSI（`*-x86_64-flutter.msi`）
- Windows x64 Sciter 便携版（`*-x86_64-sciter.exe`）
- Android arm64 签名 APK

## 更换自建服务器

在仓库 **Settings → Secrets and variables → Actions** 更新：

- `RENDEZVOUS_SERVER`：hbbs 的域名或 IP；非默认端口可写成 `host:port`，不要添加协议。
- `RS_PUB_KEY`：服务器 `id_ed25519.pub` 的完整内容。

OSS Server 不需要 `API_SERVER`。更新 Secret 后，必须推送一个新标签重新编译；已经发布或安装的客户端不会自动改变内置服务器。

## 发布修订版

同一 RustDesk 版本的自定义修订号依次递增，例如：

```powershell
git tag -a 1.4.7-2 -m "RustDesk 1.4.7 custom build 2"
git push origin 1.4.7-2
```

标签会触发 `Flutter Tag Build`，构建结果自动上传到同名 GitHub Release。

## 跟随官方升级

```powershell
git fetch upstream --tags
git switch -c custom/新版本 upstream/对应提交或官方标签
```

在新分支重新应用自定义工作流改动并验证后，推送 `新版本-1` 标签。不要直接在旧版本分支合并整个官方 `master`，这样更容易保留可复现的发布基线。

## 签名备份

本机签名备份位于 `D:\Project\rustdesk-signing-backup`，不属于 Git 仓库：

- Windows PFX 和公共证书
- Android JKS keystore
- 由当前 Windows 用户 DPAPI 加密的密码文件

Android keystore 丢失后，新 APK 将无法覆盖升级现有安装。请将整个目录另行离线备份，绝对不要提交到 Git 或上传为 Release 附件。
