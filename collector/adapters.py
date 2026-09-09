"""Attachment discovery from the official HTML, without guessed file IDs."""
import re
from urllib.parse import urlencode, urljoin, urlparse
from bs4 import BeautifulSoup


def discover(html: str, source_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    host = urlparse(source_url).hostname or ""
    found = []
    for a in soup.select("a[href]"):
        href = a["href"]
        title = a.get_text(" ", strip=True)
        url = None
        if host.endswith("motir.go.kr") and "/attach/down/" in href:
            url = urljoin(source_url, href)
        elif host.endswith("kpx.or.kr") and "boardDownload.es" in href:
            url = urljoin(source_url, href)
            title = a.parent.get_text(" ", strip=True)
        elif host.endswith("mcee.go.kr"):
            match = re.search(r"ajaxFileDownLoad\('(\d+)'\s*,\s*'(\d+)'\)", href)
            if match:
                url = urljoin(source_url, f"/home/file/readDownloadFile.do?fileId={match[1]}&fileSeq={match[2]}")
        elif host.endswith("kepco.co.kr"):
            # The official SingleFileUpload script names these two parameters.
            # GET is supported; URL-encode '+' and '/' in the opaque identifiers.
            match = re.search(r"G_FILE\.downloadFile\('([^']+)'\s*,\s*'([^']+)'\)", href)
            if match:
                query = urlencode({"fileNo": match[1], "fileSeq": match[2]})
                url = urljoin(source_url, "/c2r/FileDownload.do?" + query)
        if url and not any(x["url"] == url for x in found):
            found.append({"url": url, "title": title})
    return found
