# MyRoom
> 2021-2022 同济大学数据库系统原理课程设计：**学校教室管理系统**
>
> **P.S. 更多项目材料和课程作业，请联系邮箱 rayhuc@163.com，并备注说明来意**

<br/>

### 基本信息

- 作者：Ray
- 环境：Pipenv 环境管理
- 时间：2022-06-29
- 备注：原创项目，代码较多，数据结构较复杂，报告和其他材料请联系邮箱；

<br/>

### 代码特点

- Flask 框架，界面较好；
- 完成较多功能，具有完整的体系；
- 代码工程管理，结构完整，结构良好，扩展性强；

<br/>

### 程序运行

1. 将项目完整的克隆到一个文件夹（`git clone` 到一个文件夹）；
2. cd 到 `Project 文件夹`, 执行 `pipenv sync --dev`, 安装虚拟环境；
3. 执行 `pipenv shell` 启动虚拟环境；
4. 执行 `flask initdb` 初始化数据库, 接着执行 `flask initdata` 创建虚拟数据；
5. 执行 `flask run` 启动网页；
6. 管理账号：1952100 - password；师生账号：(在 *data-dev.db* 里看) - 20220310

P.S. 开发时库版本都在 *Pipfile.lock* 中，2023 年 4 月测试时部分库已更新，不 sync 会有 bug.

<br/>

### 不太重要的说明

- 该项目的资料和课程作业都是 **Free** 的，发到邮箱的我都会回复的:smile:
- **But,** 这个邮箱是个人的办公邮箱，大概一周查看 1~2 次的样子，所以可能回复不是很及时:cry:
