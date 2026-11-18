"use strict";

// 2048 characters is the widely used practical limit for URLs
// (older browsers, sitemaps, and many servers/CDNs cap around this length).
const MAX_URL_LENGTH = 2048;
const ALLOWED_PROTOCOLS = ["http:", "https:"];
const REQUEST_TIMEOUT_MS = 10000;

const form = document.getElementById("shorten-form");
const input = document.getElementById("long_url");
const button = form.querySelector("button[type='submit']");
const result = document.getElementById("result");

/**
 * Clean up and validate user input.
 * Returns { url } on success or { error } on failure.
 */
function validateUrl(raw) {
  // Strip leading/trailing whitespace plus invisible characters that often
  // sneak in through copy/paste (zero-width spaces, BOM).
  const value = raw.replace(/[​-‍﻿]/g, "").trim();

  if (!value) {
    return { error: "Please enter a URL." };
  }
  if (value.length > MAX_URL_LENGTH) {
    return { error: `URL is too long (max ${MAX_URL_LENGTH} characters).` };
  }
  // Reject whitespace and control characters anywhere inside the URL.
  if (/[\s\u0000-\u001F\u007F]/.test(value)) {
    return { error: "URL cannot contain spaces or control characters." };
  }

  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    return { error: "Please enter a full URL, including http:// or https://." };
  }

  // Only allow web links: blocks javascript:, data:, file:, etc.
  if (!ALLOWED_PROTOCOLS.includes(parsed.protocol)) {
    return { error: "Only http:// and https:// URLs are allowed." };
  }
  // Embedded credentials (https://user:pass@host) are a common phishing trick.
  if (parsed.username || parsed.password) {
    return { error: "URLs containing usernames or passwords are not allowed." };
  }
  // Require a real-looking host: a domain with a TLD, or localhost.
  const host = parsed.hostname;
  if (!host || (host !== "localhost" && !host.includes("."))) {
    return { error: "Please enter a URL with a valid domain name." };
  }

  // Use the browser-normalized form (e.g. lowercased host, encoded chars).
  const normalized = parsed.href;
  if (normalized.length > MAX_URL_LENGTH) {
    return { error: `URL is too long (max ${MAX_URL_LENGTH} characters).` };
  }
  return { url: normalized };
}

/** Show an error message under the form. */
function showError(message) {
  result.replaceChildren();
  result.className = "result result--error";
  const p = document.createElement("p");
  p.textContent = message; // textContent, never innerHTML: no injected markup
  result.appendChild(p);
  result.hidden = false;
}

/** Show the shortened URL under the form, with a copy button. */
function showResult(shortUrl) {
  result.replaceChildren();
  result.className = "result result--success";

  const label = document.createElement("p");
  label.className = "result-label";
  label.textContent = "Your short URL:";

  const row = document.createElement("div");
  row.className = "result-row";

  const link = document.createElement("a");
  link.textContent = shortUrl;
  link.href = shortUrl;
  link.target = "_blank";
  link.rel = "noopener noreferrer";

  const copyBtn = document.createElement("button");
  copyBtn.type = "button";
  copyBtn.className = "copy-btn";
  copyBtn.textContent = "Copy";
  copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      copyBtn.textContent = "Copied!";
    } catch {
      copyBtn.textContent = "Copy failed";
    }
    setTimeout(() => { copyBtn.textContent = "Copy"; }, 1500);
  });

  row.append(link, copyBtn);
  result.append(label, row);
  result.hidden = false;
}

function setLoading(isLoading) {
  button.disabled = isLoading;
  input.disabled = isLoading;
  button.textContent = isLoading ? "Shortening…" : "Shorten";
}

/** Only trust the server's response if it is a proper http(s) URL. */
function isSafeHttpUrl(value) {
  if (typeof value !== "string" || value.length > MAX_URL_LENGTH) return false;
  try {
    return ALLOWED_PROTOCOLS.includes(new URL(value).protocol);
  } catch {
    return false;
  }
}

async function shorten(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch("/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ url }),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error(`Server error (${response.status}). Please try again.`);
    }

    const data = await response.json();
    if (!isSafeHttpUrl(data?.hashed_url)) {
      throw new Error("Unexpected response from server.");
    }
    return data.hashed_url;
  } catch (err) {
    if (err.name === "AbortError") {
      throw new Error("Request timed out. Please try again.");
    }
    if (err instanceof TypeError) {
      throw new Error("Could not reach the server. Check your connection.");
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (button.disabled) return; // ignore double submits

  const { url, error } = validateUrl(input.value);
  if (error) {
    showError(error);
    input.setAttribute("aria-invalid", "true");
    input.focus();
    return;
  }
  input.removeAttribute("aria-invalid");

  setLoading(true);
  try {
    const shortUrl = await shorten(url);
    showResult(shortUrl);
  } catch (err) {
    showError(err.message || "Something went wrong. Please try again.");
  } finally {
    setLoading(false);
  }
});

// Clear the error state as soon as the user starts editing again.
input.addEventListener("input", () => {
  if (input.getAttribute("aria-invalid") === "true") {
    input.removeAttribute("aria-invalid");
    result.hidden = true;
  }
});
