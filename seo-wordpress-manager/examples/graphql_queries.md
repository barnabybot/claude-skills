# GraphQL Queries for WordPress SEO

Useful queries for the WPGraphQL + Yoast SEO setup.

## Fetch Posts with SEO Data

```graphql
query GetPostsWithSEO($first: Int = 100, $after: String) {
  posts(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      databaseId
      title
      slug
      uri
      date
      categories {
        nodes {
          name
          slug
        }
      }
      seo {
        title
        metaDesc
        focuskw
        opengraphTitle
        opengraphDescription
        opengraphImage {
          sourceUrl
        }
        twitterTitle
        twitterDescription
        canonical
        readingTime
      }
    }
  }
}
```

## Fetch Single Post SEO

```graphql
query GetPostSEO($id: ID!) {
  post(id: $id, idType: DATABASE_ID) {
    databaseId
    title
    content
    seo {
      title
      metaDesc
      focuskw
      opengraphTitle
      opengraphDescription
      canonical
      cornerstone
      readingTime
    }
  }
}
```

## Fetch Posts by Category

```graphql
query GetPostsByCategory($categorySlug: String!, $first: Int = 50) {
  posts(first: $first, where: { categoryName: $categorySlug }) {
    nodes {
      databaseId
      title
      seo {
        title
        metaDesc
        focuskw
      }
    }
  }
}
```

## Update Post SEO (Custom Mutation)

Requires the custom mutation from SKILL.md's prerequisites.

```graphql
mutation UpdatePostSeo(
  $postId: Int!
  $title: String
  $metaDesc: String
  $focusKeyphrase: String
) {
  updatePostSeo(input: {
    postId: $postId
    title: $title
    metaDesc: $metaDesc
    focusKeyphrase: $focusKeyphrase
  }) {
    success
    post {
      databaseId
      title
      seo {
        title
        metaDesc
        focuskw
      }
    }
  }
}
```

### Example Variables

```json
{
  "postId": 101,
  "title": "Python Data Analysis Guide: Pandas, NumPy & Matplotlib",
  "metaDesc": "Master Python data analysis with this hands-on guide.",
  "focusKeyphrase": "Python data analysis"
}
```

## Fetch Pages with SEO

```graphql
query GetPagesWithSEO($first: Int = 50) {
  pages(first: $first) {
    nodes {
      databaseId
      title
      slug
      seo {
        title
        metaDesc
        focuskw
      }
    }
  }
}
```

## Check for Missing SEO Data

```graphql
query FindMissingSEO($first: Int = 100) {
  posts(first: $first) {
    nodes {
      databaseId
      title
      seo {
        title
        metaDesc
        focuskw
      }
    }
  }
}
```

Then filter in your client:
```javascript
const missingMeta = posts.filter(p => 
  !p.seo.title || 
  !p.seo.metaDesc || 
  !p.seo.focuskw
);
```

## Fetch Revisions (for Rollback)

```graphql
query GetPostRevisions($id: ID!) {
  post(id: $id, idType: DATABASE_ID) {
    title
    revisions(first: 10) {
      nodes {
        databaseId
        date
        content
      }
    }
  }
}
```

## Using with cURL

```bash
# Set variables
GRAPHQL_URL="https://your-site.com/graphql"
USERNAME="your-user"
APP_PASSWORD="xxxx xxxx xxxx xxxx"

# Encode credentials
AUTH=$(echo -n "$USERNAME:$APP_PASSWORD" | base64)

# Run query
curl -s "$GRAPHQL_URL" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ posts(first: 5) { nodes { databaseId title seo { title metaDesc } } } }"}'
```

## Tips

- **Pagination**: Use `after: $cursor` with `pageInfo.endCursor` for large sites
- **Rate limits**: WordPress typically handles ~100 requests/minute safely
- **Caching**: Add `?nocache=1` for fresh data during testing
- **Auth**: Application Passwords work best for API access
