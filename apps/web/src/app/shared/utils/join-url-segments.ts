export function joinUrlSegments(...segments: readonly string[]): string {
  return segments
    .filter((segment) => segment.length > 0)
    .map((segment, index) => {
      if (index === 0) {
        return segment.replace(/\/+$/, '');
      }

      return segment.replace(/^\/+/, '').replace(/\/+$/, '');
    })
    .join('/');
}
