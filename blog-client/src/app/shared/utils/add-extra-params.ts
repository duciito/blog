export function addExtraParams(url, extraParams) {
    if (extraParams) {
      for (const key in extraParams) {
        url += `?${key}=${extraParams[key]}`;
      }
    }

    return url;
}
