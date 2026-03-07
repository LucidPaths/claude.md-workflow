# Pull Request Guidelines

When creating pull requests for this repository, always include detailed update notes so reviewers can quickly understand what changed.

## PR Description Format

Use this structure for all PR descriptions:

```markdown
## Summary
Brief 1-2 sentence overview of what this PR accomplishes.

## Changes
- **[Category]**: Description of change
- **[Category]**: Description of change
- ...

## Technical Details
(Optional) Any implementation notes, architectural decisions, or important context.

## Testing
How to verify the changes work:
1. Step one
2. Step two
3. ...
```

## Categories to Use

- **Added**: New features or files
- **Changed**: Modifications to existing functionality
- **Fixed**: Bug fixes
- **Removed**: Deleted code or features
- **Updated**: Dependency updates, version bumps
- **Refactored**: Code restructuring without behavior change
- **Docs**: Documentation changes

## Example

```markdown
## Summary
Add user authentication with JWT tokens.

## Changes
- **Added**: Login and register API endpoints
- **Added**: JWT token generation and validation middleware
- **Changed**: Protected routes now require Authorization header
- **Fixed**: Password hashing uses bcrypt instead of plaintext

## Technical Details
- Tokens expire after 24 hours, refresh tokens after 7 days
- Password requirements: min 8 chars, 1 uppercase, 1 number
- Rate limiting: 5 failed attempts per 15 minutes per IP

## Testing
1. Run `npm test` to verify all auth tests pass
2. Start dev server with `npm run dev`
3. POST to `/api/register` with email and password
4. POST to `/api/login` and verify JWT is returned
5. Access protected route with and without token
```

## Commit Messages

Follow conventional commit style:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code restructuring
- `chore:` Maintenance tasks

Keep the first line under 72 characters, add details in the body if needed.
