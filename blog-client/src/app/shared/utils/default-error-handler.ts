export function defaultErrorHandler(error, toastrInstance) {
  const errors: any = [...Object.values(error.error || error)].reduce(
    (acc: string[], val: string) => acc.concat(val), []
  );

  errors.forEach(error => toastrInstance.error(error));
}
