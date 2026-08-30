# Docker 簡介

本章將帶領你進入 **Docker** 的世界。

> **版本提示**：本書內容及範例基於 **Docker Engine v29.x** 及以上版本。值得注意的是，自 Docker Engine v29 起，官方在全新安裝情境下**預設啟用 `containerd image store` 作為映像檔儲存後端**（取代傳統 classic store 路徑下的 graph driver 體系）。這項底層革新大幅增強了 Docker 對多架構映像檔（Multi-platform）以及軟體供應鏈安全中繼資料（Attestations、SBOM、Provenance）的本地支援原生性。

## 本章內容

* [快速上手](quickstart.md)
  * 透過一個簡單的 Web 應用範例，帶你快速體驗 Docker 的核心流程：建立映像檔、執行容器。

* [什麼是 Docker](what.md)
  * 介紹 Docker 的起源、發展歷程以及其背後的核心技術（Cgroups、Namespaces、UnionFS，以及 `containerd` 引擎的演進）。
  * 了解 Docker 是如何改變軟體交付方式的。

* [為什麼要用 Docker](why.md)
  * 對比傳統虛擬機技術，闡述 Docker 在啟動速度、資源使用率、交付效率等方面的巨大優勢。
  * 探討 Docker 在 DevOps、微服務架構中的關鍵作用。

## 學習目標

透過本章的學習，你將能夠：

1. 理解 Docker 的核心概念與架構。
2. 明白 Docker 解決了現代軟體開發與維運中的哪些痛點。
3. 建立起對容器技術的初步認知，為後續的實戰操作打下基礎。

好吧，讓我們帶著問題開始這神奇之旅。
