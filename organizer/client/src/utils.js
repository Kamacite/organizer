export function sanitize(target) {
    return DOMPurify.sanitize(target)
}