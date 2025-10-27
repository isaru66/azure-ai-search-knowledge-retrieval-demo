# Azure AI Search – Knowledge Retrieval Demo (Minimal)

Production-ready Next.js app demonstrating two retrieval patterns:
1. Azure AI Search Knowledge Bases (answer synthesis, citations)
2. Azure AI Foundry Assistants (MCP tool integration)

This is the lightweight README. For full guides see:
- Extended deployment: `AZURE_DEPLOYMENT_GUIDE.md`
- Authentication details: `docs/AUTHENTICATION.md`
- Original comprehensive README: See commit history if needed.

## Quick Start

```bash
git clone https://github.com/farzad528/azure-ai-search-knowledge-retrieval-demo.git
cd azure-ai-search-knowledge-retrieval-demo
npm install
cp .env.example .env.local
# edit .env.local with your values
npm run dev
```
Open http://localhost:3000

### Required Environment Variables
Minimum for the `/test` knowledge base playground:
```bash
AZURE_SEARCH_ENDPOINT=https://<your-search>.search.windows.net
AZURE_SEARCH_API_KEY=<admin-or-query-key>
AZURE_SEARCH_API_VERSION=2025-11-01-preview
NEXT_PUBLIC_AZURE_OPENAI_ENDPOINT=https://<your-openai>.openai.azure.com
AZURE_OPENAI_API_KEY=<openai-key>
```
Optional (enables Assistants `/agents`):
```bash
FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
FOUNDRY_API_VERSION=2025-05-01
AZURE_AUTH_METHOD=service-principal
AZURE_TENANT_ID=<tenant>
AZURE_CLIENT_ID=<appId>
AZURE_CLIENT_SECRET=<secret>
```

### Create a Knowledge Base (UI)
1. Run locally
2. Navigate to `/knowledge`
3. Add sources (blob / search index / web crawl)
4. Configure output modality (answerSynthesis or extractive)
5. Test queries in `/test`

## Minimal API Usage (Retrieve)

Example request (cURL) with runtime controls reflected:
```bash
curl -X POST "$AZURE_SEARCH_ENDPOINT/agents/my-agent/retrieve?api-version=2025-11-01-preview" \
  -H "api-key: $AZURE_SEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role":"user","content":"Summarize recent revenue highlights."}],
    "outputMode": "answer",
    "retrievalReasoningEffort": {"kind": "standard"},
    "knowledgeSourceParams": {
      "alwaysQuerySource": true,
      "includeReferences": true,
      "maxSubQueries": 3
    }
  }'
```

TypeScript (fetch) snippet:
```ts
const resp = await fetch(`${process.env.AZURE_SEARCH_ENDPOINT}/agents/my-agent/retrieve?api-version=2025-11-01-preview`, {
  method: 'POST',
  headers: {
    'api-key': process.env.AZURE_SEARCH_API_KEY!,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    messages: [{ role: 'user', content: 'Summarize recent revenue highlights.' }],
    outputMode: 'answer',
    retrievalReasoningEffort: { kind: 'standard' },
    knowledgeSourceParams: {
      alwaysQuerySource: true,
      includeReferences: true,
      maxSubQueries: 3
    }
  })
});
const data = await resp.json();
```

Notes:
- Omit boolean params if false; send only those set to true.
- Use `outputMode: 'answer'` (synthesized) or `'extractive'` (raw chunks).
- `retrievalReasoningEffort.kind` controls sub-query reasoning (e.g. `none | standard | enhanced`).

## Security (Essentials)
- Keep keys in environment variables; never commit them.
- View Code modal masks sensitive headers (toggle to reveal). Treat masked values as secrets.
- Prefer Service Principal (`AZURE_AUTH_METHOD=service-principal`) for automatic token refresh.
- Rotate Search and OpenAI keys periodically.

## Lightweight Deployment Options
- Vercel: Fastest path. Set env vars in project settings and deploy.
- Azure Static Web App or App Service: Use same env names; consider Managed Identity where feasible.
See `AZURE_DEPLOYMENT_GUIDE.md` for full scripts and alternatives.

## Troubleshooting (Quick)
| Issue | Fix |
|-------|-----|
| 401 (Search) | Check API key + preview API version |
| 401 (Foundry) | SP credentials or expired manual token |
| Empty KB list | Verify endpoint + key + API version |
| No citations | Ensure `includeReferences` true and sources ingested |

## Contributing
PRs welcome. Keep changes small and typed. Run `npm run build` before submitting.

## License
MIT – see `LICENSE`.

## Resources
Azure AI Search Docs: https://learn.microsoft.com/azure/search/
Azure AI Foundry Assistants: https://learn.microsoft.com/azure/ai-services/agents/
Model Context Protocol: https://modelcontextprotocol.io/

---
If you need the full original detailed README, retrieve it from prior commits or project history.
