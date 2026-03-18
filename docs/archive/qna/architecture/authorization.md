# Authorization

## 2. Authentication, users, roles, and provisioning
### 8. Should there be a separate application user model?
**Decision:** Yes. The system has an application user/profile model in the app database, linked 1:1 to the Supabase Auth user id. This app user is the source of truth for roles, effective permissions, and audit identity.

### 9. What is the authorization model?
**Decision:** The system is capability-based. Roles are predefined bundles of capabilities. The schema supports direct per-user capability grants for future evolution, but v1 will not expose or use that feature.

### 10. Are role definitions editable in v1?
**Decision:** No. In v1, roles, role-capability mappings, and default user-role assignments are seeded/static. If changes are needed, they will be made directly in the database as an operational action.

### 11. Is there a superadmin concept?
**Decision:** Yes. Superadmin is modeled as a role bundle/capability set, not as a special code path spread across the application. It includes admin capabilities plus user-management and future app-management capabilities.

### 12. How is the first superadmin bootstrapped?
**Decision:** The first superadmin is created through a seed/migration path, with manual DB intervention documented as a break-glass recovery procedure.

### 13. Should users self-register?
**Decision:** No. There is no public self-registration. Authenticated application users are provisioned explicitly.

### 14. Who is allowed to provision users in v1?
**Decision:** Only the superadmin can create users.

### 15. What user management exists in the app in v1?
**Decision:** v1 includes only a **minimal superadmin UI** for creating a user with an email, a password, and a seeded role. Users are active immediately on creation.

### 16. Does the minimal user UI also provision the identity-provider account?
**Decision:** Yes. The api provisions the Auth identity and the linked application user in a single orchestrated workflow.

### 17. What login method is used in v1?
**Decision:** Email and password.

### 18. Is there email verification, invitation flow, or reset/set-password flow in v1?
**Decision:** No. v1 keeps provisioning extremely minimal: the superadmin creates the user with a password, and credentials are handed over manually offline.

### 19. How are cross-system provisioning failures handled?
**Decision:** User provisioning is treated as a two-step external workflow with best-effort compensation. The api creates the identity-provider account first, then creates the application user. If the second step fails, the api attempts to remove the identity-provider account and logs any unrecoverable partial failure clearly.

### 20. Should auth be abstracted for future SSO/custom identity?
**Decision:** Yes. Authentication and provisioning sit behind explicit identity-provider adapters so Supabase Auth can be replaced later without touching application/domain logic.

### 21. Should capabilities be cached in process as effective permissions?
**Decision:** No separate runtime cache of effective user permissions is introduced as an architectural requirement. The hardcoded part is only the capability vocabulary. Role/user assignments remain data-driven.


## Related product clarifications
### 18) How should user accounts work?
**Answer:** The product should be designed for **individual accounts** for admins and judges. In practice, admins may do most of the work, judges may share usage patterns, or judges may not always use the software directly, but the model should still support individual identities and auditability.

### 39) What permission model should the app use?
**Answer:** The app should use **capability-based authorization**. Roles are just a convenient way to assign bundles of capabilities.

### 40) What capability set is needed in v1?
**Answer:** The capability set should include:
- manage season config
- manage tournament pairings
- start game
- complete game
- mark under examination
- resolve under examination
- enter and edit results
- set Jolly usage
- apply manual standings adjustments
- view audit log
- review post-completion edits and move pending admin review back to completed

### 41) Who can mark a game under examination and resolve it?
**Answer:** **Judges and admins** can do both.

### 46) What default role bundles should exist on top of capabilities?
**Answer:** Default bundles are:
- **Admin**: all capabilities
- **Judge**: operational capabilities (results, states, Jolly, pairings, etc.)
- **Public**: no login, read-only
