# eHub

**eHub** is a lightweight, standalone Model Context Protocol (MCP) server designed to seamlessly bridge LibreChat with external APIs. 

## 🎯 Project Goal
To serve as a modular, unified translation hub that expands LibreChat's capabilities (Images, Voice, Search, etc.) without requiring *any* modifications to LibreChat's core source code. It runs as an independent microservice container on the same Docker network.

## ✨ Current Functionality
* **OpenRouter Image Generation:** Intercepts image generation prompts from LibreChat, routes them to OpenRouter models (Flux, Stable Diffusion, etc.), downloads the resulting image URLs, and automatically encodes them into the strict Base64 format required for native LibreChat rendering. 
* **Smart Model Routing:** Uses a fast default model, but allows the LLM to intelligently switch to specific models if requested by the user.

## 🚀 Future Scope
Built from day one with a stateless, asynchronous, and pluggable architecture, eHub is designed to easily scale into a multi-tool hub supporting more non-text tasks for AI agents.