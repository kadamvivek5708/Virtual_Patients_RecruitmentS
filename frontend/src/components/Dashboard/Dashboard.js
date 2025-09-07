// src/components/WelcomePage.js

import React from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
  import { Link } from "react-router-dom";
import { 
  FaUserMd, 
  FaShieldAlt, 
  FaRocket, 
  FaHandHoldingHeart, 
  FaVial, 
  FaFileMedicalAlt, 
  FaClipboardCheck 
} from 'react-icons/fa';
import styles from './WelcomePage.module.css';

const WelcomePage = () => {
  const navigate = useNavigate();

  const handleCTA = () => {
    const role = localStorage.getItem("role");
    if (role === "admin") {
      navigate("/bulk-upload");
    } else if (role === "patient") {
      navigate("/dashboard");
    } else {
      navigate("/register"); // not logged in
    }
  };

  return (
    <div className={styles.welcomePage}>
      
      {/* Hero Section */}
      <header className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>Pioneering the Future of Medicine, Together.</h1>
          <p className={styles.heroSubtitle}>
            Join our virtual clinical trials to access cutting-edge treatments and contribute 
            to groundbreaking medical research from the comfort of your home.
          </p>
          <div className={styles.quickActions}>
            <NavLink to="/patient-application" className={styles.quickBtn}>Apply now</NavLink>
            <NavLink to="/my-applications" className={styles.quickBtn}>My applications</NavLink>
          </div>

        </div>
      </header>

      {/* Features Section */}
      <section className={styles.features}>
        <div className={styles.featureCard}>
          <FaUserMd className={styles.featureIcon} />
          <h3 className={styles.featureTitle}>Expert Medical Teams</h3>
          <p>Our trials are led by world-class physicians and researchers dedicated to patient safety and care.</p>
        </div>
        <div className={styles.featureCard}>
          <FaShieldAlt className={styles.featureIcon} />
          <h3 className={styles.featureTitle}>Data Security & Privacy</h3>
          <p>We use state-of-the-art technology to ensure your personal health information is always protected.</p>
        </div>
        <div className={styles.featureCard}>
          <FaRocket className={styles.featureIcon} />
          <h3 className={styles.featureTitle}>Accelerate Research</h3>
          <p>By participating, you help speed up the development of new, life-saving therapies for everyone.</p>
        </div>
      </section>

      {/* How It Works Section */}
      <section className={styles.howItWorks}>
        <h2 className={styles.sectionTitle}>A Simple Path to Participation</h2>
        <div className={styles.timeline}>
          <div className={styles.timelineItem}>
            <div className={styles.timelineIcon}><FaFileMedicalAlt /></div>
            <div className={styles.timelineContent}>
              <h4>1. General Screening</h4>
              <p>Complete a simple online form to determine your initial eligibility for our research programs.</p>
            </div>
          </div>
          <div className={styles.timelineItem}>
            <div className={styles.timelineIcon}><FaVial /></div>
            <div className={styles.timelineContent}>
              <h4>2. Trial Matching</h4>
              <p>If eligible, you'll be invited to apply for specific trials that match your health profile.</p>
            </div>
          </div>
          <div className={styles.timelineItem}>
            <div className={styles.timelineIcon}><FaClipboardCheck /></div>
            <div className={styles.timelineContent}>
              <h4>3. Enrollment</h4>
              <p>Our team will guide you through the final steps to officially enroll in a groundbreaking study.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className={styles.testimonials}>
        <h2 className={styles.sectionTitle}>What Our Participants Say</h2>
        <div className={styles.testimonialGrid}>
          <div className={styles.testimonialCard}>
            <blockquote>
              "Participating in a virtual trial was easier than I ever imagined. 
              I felt like I was making a real difference without disrupting my life."
            </blockquote>
            <cite>— Sarah J., Hypertension Trial Participant</cite>
          </div>
          <div className={styles.testimonialCard}>
            <blockquote>
              "The medical team was incredibly supportive. Knowing my data was secure gave me complete peace of mind throughout the process."
            </blockquote>
            <cite>— David L., Arthritis Trial Participant</cite>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className={styles.finalCta}>
        <div className={styles.ctaContent}>
          <FaHandHoldingHeart className={styles.ctaIcon} />
          <h2>Ready to Shape the Future of Health?</h2>
          <p>Your participation is vital. Find a clinical trial that's right for you and take the first step today.</p>
      
            
            <NavLink to="/patient-application" className={styles.ctaButton}>Go to Patient Application</NavLink>

            
          
        </div>
      </section>
    </div>
  );
};

export default WelcomePage;
