---
layout: post
title: GitHub Actions构建失败排查记
slug: github-actions-gou-jian-shi-bai-pai-cha-ji
date: 2026-04-04 23:48
status: publish
author: jerfo0
categories: 
  - 技术
tags: 
  - GitHub Actions
  - CI/CD
  - 排错
  - Maverick
excerpt: 网站长时间没更新，原来是GitHub Actions构建失败，记录四个问题的排查修复过程。
---

当本网站长时间没有更新时，根本原因是 GitHub Actions 构建失败，新文章 push 上去之后，自动构建流程一直在报错，所以网站内容没有更新。

## 修复了四个问题

### 1. Python 版本过旧

ci.yml 里指定的是 python 3.7，但 GitHub Actions 的运行环境已经不再提供 3.7，最低只有 3.10，导致构建直接失败。

→ 改成 `python-version: "3.10"` 解决。

### 2. Actions 依赖版本过旧

`actions/checkout@v2`、`actions/setup-python@v1` 以及部署用的 `docker://peaceiris/gh-pages:v2` 都是几年前的旧版本，与现在的 runner 环境不兼容。

→ 全部升级到最新版本解决。

### 3. Submodule 拉取没有认证

Maverick 是以 git submodule 方式引入的，checkout@v4 默认不带认证 token 去拉取子模块，导致 git 报 exit code 128 错误。

→ 在 checkout 步骤加上 `submodules: recursive` 和 `token: ${{ secrets.PERSONAL_TOKEN }}` 解决。

### 4. PERSONAL_TOKEN 已过期

仓库里存的 token 已经失效，导致认证始终不通过。

→ 在 GitHub 重新生成 token 并更新 Secret 解决。

## 经验总结

以后如果网站又没更新，第一步就去 https://github.com/jerfo0/9i57/actions 看 Actions 有没有报错，能省很多排查时间。

再次感谢 Claude 强大的功能，膜拜！！！