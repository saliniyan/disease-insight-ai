import React from "react";
import "./Blog.css";

const Blog = () => {
  const blogPosts = [
    {
      title: "Understanding Common Health Symptoms",
      date: "February 2, 2025",
      excerpt: "Learn about the most common health symptoms and what they might indicate...",
      category: "Health Education",
    },
    {
      title: "The Importance of Early Disease Detection",
      date: "February 1, 2025",
      excerpt: "Early detection of diseases can significantly improve treatment outcomes...",
      category: "Medical Insights",
    },
    {
      title: "Natural Remedies for Common Ailments",
      date: "January 30, 2025",
      excerpt: "Discover effective natural remedies that can help alleviate common health issues...",
      category: "Natural Health",
    },
  ];

  return (
    <div className="blog-container">
      <h1>Health Blog</h1>
      <div className="blog-list">
        {blogPosts.map((post, index) => (
          <article key={index} className="blog-card">
            <div className="blog-header">
              <h2>{post.title}</h2>
              <span className="blog-category">{post.category}</span>
            </div>
            <p>{post.excerpt}</p>
            <div className="blog-footer">
              <span className="blog-date">{post.date}</span>
              <button className="read-more">Read More →</button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
};

export default Blog;
