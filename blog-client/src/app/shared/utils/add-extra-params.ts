export function addExtraParams(url, extraParams) {
    if (extraParams) {
      url += '?';
      for (const key in extraParams) {
        url += `&${key}=${extraParams[key]}`;
      }
    }

    return url;
}
