# BJTU-Homework-Tracker

![Visitors](https://api.visitorbadge.io/api/visitors?path=ymzhang-cs%2FBJTU-Homework-Tracker&countColor=%23263759)

![Latest Tag](https://img.shields.io/github/v/tag/ymzhang-cs/BJTU-Homework-Tracker)
![GitHub contributors](https://img.shields.io/github/contributors/ymzhang-cs/BJTU-Homework-Tracker)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/ymzhang-cs/BJTU-Homework-Tracker)
![GitHub last commit](https://img.shields.io/github/last-commit/ymzhang-cs/BJTU-Homework-Tracker)
![GitHub](https://img.shields.io/github/license/ymzhang-cs/BJTU-Homework-Tracker)


北京交通大学智慧课程平台作业抓取

支持在登录后自动化抓取作业列表，在筛选后进行可视化输出。

支持的登录方式：

- 智慧课程平台账号登录
- MIS 系统登录
- Cookie登录

支持的作业筛选方式

- 按完成状态：未完成/已完成/全部
- 按课程名：支持白名单/黑名单
- 按距离截止时间
- 按已过期时间

支持的显示/保存结果方式

- HTML页面渲染
- 纯文本显示

## 快速上手

**0. 克隆仓库**

```bash
git clone https://github.com/ymzhang-cs/BJTU-Homework-Tracker.git
cd BJTU-Homework-Tracker
```

**1. 安装依赖**

```bash
pip install -r requirements.txt
```

**2. 配置 config.yaml（可选，推荐）**

工具支持 config 工作流配置和命令行实时配置两种控制方式。后者直接跳至第3步即可，下面介绍 config 配置方式。

拷贝 config_sample.yaml 为 config.yaml，并且参考相关注释填写即可。

**3. 运行 run.py**

```bash
python run.py
```

> [!NOTE]
> 如果选择使用 MIS 系统登录，请确保已经安装了 Chrome 浏览器或 Edge 浏览器（后续会支持更多）。
> 
> 第一次使用会自动下载对应的 WebDriver，如果下载失败请手动下载并放置在浏览器根目录（如 `C:\Program Files\Google\Chrome\Application`）下。

## TODO

- [ ] 使用 Schema 验证配置文件 [#8](https://github.com/ymzhang-cs/BJTU-Homework-Tracker/issues/8)
- [ ] 更好的 WebDriver 配置模式 [#9](https://github.com/ymzhang-cs/BJTU-Homework-Tracker/issues/9)
- [ ] 考虑使用 PyInquirer 交互式配置 [#16](https://github.com/ymzhang-cs/BJTU-Homework-Tracker/issues/16)

## Contributing

欢迎提交 PR 和 issue，为这个项目贡献你的力量。

如果你有任何问题或者想法，请提交 issue。 若要认领 issue，请在 issue 下评论，我们会将 issue 分配给你。
如果有想要实现的功能，请先提交 issue 并认领，然后再提交 PR。

与 issue 关联的 PR 请在提交 PR 时在 PR 描述中注明 `Fixes #xx`，以便 issue 关联。没有关联任何 issue 的 PR 会被关闭。

## License

我们采用 [MIT](LICENSE) 开源许可证。

## References

- [如何获取Cookie](FOR_NEWERS.md)
