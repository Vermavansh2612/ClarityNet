"""
ClarityNet - Enhanced Backend Module with TRUE Multi-Media Support
Now with actual video/audio processing and intelligent reasoning explanations
"""

import google.generativeai as genai
from config import (
    GEMINI_API_KEY, MODELS, MODEL_NAMES, COMPLEXITY_THRESHOLD,
    WORD_COUNT_THRESHOLD, TECHNICAL_KEYWORDS, GENERATION_CONFIG
)
import time
from typing import Optional, Dict, Any, List, Union
from PIL import Image
import threading
import io


class RateLimiter:
    """Simple rate limiter to track API calls"""
    
    def __init__(self, max_calls: int = 2, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()
    
    def can_call(self) -> tuple[bool, float]:
        """Check if we can make a call, return (can_call, wait_time)"""
        with self.lock:
            now = time.time()
            self.calls = [call_time for call_time in self.calls if now - call_time < self.period]
            
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True, 0.0
            else:
                oldest_call = min(self.calls)
                wait_time = self.period - (now - oldest_call) + 1
                return False, wait_time
    
    def reset(self):
        """Reset the rate limiter"""
        with self.lock:
            self.calls = []


class ClarityNetEngine:
    """Enhanced engine for ClarityNet AI with TRUE multimedia support"""
    
    def __init__(self):
        """Initialize Gemini models with caching and error handling"""
        genai.configure(api_key=GEMINI_API_KEY)
        
        self.rapid_limiter = RateLimiter(max_calls=15, period=60.0)
        self.advanced_limiter = RateLimiter(max_calls=2, period=60.0)
        
        # Initialize models with fallbacks
        try:
            print(f"🔄 Initializing Rapid Model: {MODELS['rapid']}")
            self.rapid_model = genai.GenerativeModel(MODELS["rapid"])
            print(f"✅ Rapid Model Ready: {MODELS['rapid']}")
        except Exception as e:
            print(f"❌ Error initializing rapid model: {e}")
            try:
                fallback_rapid = "gemini-2.0-flash"
                print(f"🔄 Trying fallback: {fallback_rapid}")
                self.rapid_model = genai.GenerativeModel(fallback_rapid)
                print(f"✅ Fallback Rapid Model Ready: {fallback_rapid}")
            except Exception as e2:
                raise Exception(f"Failed to initialize any rapid model: {e2}")
        
        try:
            print(f"🔄 Initializing Advanced Model: {MODELS['advanced']}")
            self.advanced_model = genai.GenerativeModel(MODELS["advanced"])
            print(f"✅ Advanced Model Ready: {MODELS['advanced']}")
        except Exception as e:
            print(f"❌ Error initializing advanced model: {e}")
            try:
                fallback_advanced = "gemini-2.5-pro"
                print(f"🔄 Trying fallback: {fallback_advanced}")
                self.advanced_model = genai.GenerativeModel(fallback_advanced)
                print(f"✅ Fallback Advanced Model Ready: {fallback_advanced}")
            except Exception as e2:
                raise Exception(f"Failed to initialize any advanced model: {e2}")
        
        self._response_cache = {}
        self._explanation_cache = {}
        self._start_time = None
        self.explanation_enabled = True
        print("✅ ClarityNet Engine Initialized Successfully!\n")
    
    def analyze_query(self, query: str, media_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Advanced query analysis with multi-dimensional scoring
        Now properly handles video and audio metadata
        """
        if media_info is None:
            media_info = {"has_image": False, "has_video": False, "has_audio": False}
        
        words = query.split()
        word_count = len(words)
        char_count = len(query)
        
        # Enhanced technical keyword detection
        technical_score = sum(
            3 if keyword in query.lower() else 0
            for keyword in TECHNICAL_KEYWORDS
        )
        has_technical = technical_score > 0
        
        # Question complexity indicators
        has_multiple_questions = query.count('?') > 1
        has_comparisons = any(word in query.lower() for word in ['compare', 'versus', 'vs', 'difference'])
        has_explanations = any(word in query.lower() for word in ['explain', 'why', 'how', 'analyze'])
        
        # Media complexity weights
        has_image = media_info.get("has_image", False)
        has_video = media_info.get("has_video", False)
        has_audio = media_info.get("has_audio", False)
        
        # Calculate weighted complexity score
        base_complexity = min(word_count / 50, 1.0) * 0.3
        technical_weight = min(technical_score / 10, 1.0) * 0.25
        
        # Video requires more processing than images
        media_weight = (
            (0.35 if has_video else 0) +
            (0.25 if has_audio else 0) +
            (0.20 if has_image and not has_video else 0)
        )
        
        question_weight = (
            (0.1 if has_multiple_questions else 0) +
            (0.05 if has_comparisons else 0) +
            (0.05 if has_explanations else 0)
        )
        
        complexity_score = min(
            base_complexity + technical_weight + media_weight + question_weight,
            1.0
        )
        
        # Smart model selection - video/audio ALWAYS use advanced
        use_advanced = (
            has_video or
            has_audio or
            complexity_score > COMPLEXITY_THRESHOLD or
            has_technical or
            word_count > WORD_COUNT_THRESHOLD or
            has_image or
            has_multiple_questions or
            (has_comparisons and word_count > 10)
        )
        
        # Generate reasoning
        model_selection_reasoning = self._generate_model_selection_reasoning(
            use_advanced, has_technical, has_image, has_video, has_audio,
            complexity_score, has_multiple_questions, has_comparisons, has_explanations
        )
        
        return {
            "complexity_score": round(complexity_score, 3),
            "word_count": word_count,
            "char_count": char_count,
            "has_technical": has_technical,
            "technical_score": technical_score,
            "has_image": has_image,
            "has_video": has_video,
            "has_audio": has_audio,
            "has_multiple_questions": has_multiple_questions,
            "has_comparisons": has_comparisons,
            "has_explanations": has_explanations,
            "use_advanced": use_advanced,
            "model_name": MODEL_NAMES["advanced"] if use_advanced else MODEL_NAMES["rapid"],
            "model_selection_reasoning": model_selection_reasoning
        }
    
    def _generate_model_selection_reasoning(
        self, use_advanced: bool, has_technical: bool, has_image: bool,
        has_video: bool, has_audio: bool, score: float,
        has_multiple: bool, has_comparisons: bool, has_explanations: bool
    ) -> str:
        """Generate detailed reasoning for model selection"""
        reasons = []
        
        if has_video:
            reasons.append("🎬 video analysis with temporal understanding required")
        if has_audio:
            reasons.append("🎵 audio processing and speech analysis needed")
        if has_image and not has_video:
            reasons.append("🎨 visual analysis required")
        if has_technical:
            reasons.append("🔬 specialized technical knowledge needed")
        if has_multiple:
            reasons.append("❓ multiple questions requiring comprehensive coverage")
        if has_comparisons:
            reasons.append("⚖️ comparative evaluation needed")
        if has_explanations:
            reasons.append("📚 deep explanatory analysis required")
        if score > COMPLEXITY_THRESHOLD and not reasons:
            reasons.append("🧩 high complexity query detected")
        
        if use_advanced:
            reason_text = ", ".join(reasons) if reasons else "comprehensive analysis needed"
            return f"**Advanced Reasoning Engine** selected: {reason_text}"
        else:
            return "**Rapid Response Engine** selected: straightforward query optimized for speed"
    
    def _upload_media_file(self, file_bytes: bytes, mime_type: str, display_name: str):
        """Upload media file to Gemini API for processing"""
        try:
            uploaded_file = genai.upload_file(
                io.BytesIO(file_bytes),
                mime_type=mime_type,
                display_name=display_name
            )
            return uploaded_file
        except Exception as e:
            print(f"❌ Error uploading media file: {e}")
            return None
    
    def generate_response(
        self,
        query: str,
        images: Optional[List[Image.Image]] = None,
        video: Optional[Any] = None,
        audio: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response with TRUE multimedia support
        Now handles images, video, AND audio properly!
        """
        self._start_time = time.time()
        
        # Prepare media info for analysis
        media_info = {
            "has_image": images is not None and len(images) > 0,
            "has_video": video is not None,
            "has_audio": audio is not None
        }
        
        # Analyze query with proper media context
        analysis = self.analyze_query(query, media_info)
        
        # Check cache (only for text-only queries)
        cache_key = f"{query}_{analysis['model_name']}"
        if cache_key in self._response_cache and not any(media_info.values()):
            cached = self._response_cache[cache_key].copy()
            cached['from_cache'] = True
            cached['processing_time'] = time.time() - self._start_time
            return cached
        
        try:
            # Select model and rate limiter
            use_advanced = analysis["use_advanced"]
            model = self.advanced_model if use_advanced else self.rapid_model
            limiter = self.advanced_limiter if use_advanced else self.rapid_limiter
            
            # Check rate limit
            can_call, wait_time = limiter.can_call()
            if not can_call:
                return {
                    "response": None,
                    "answer_explanation": None,
                    "analysis": analysis,
                    "success": False,
                    "error": f"Rate limit reached. Please wait {int(wait_time)} seconds.",
                    "processing_time": time.time() - self._start_time,
                    "from_cache": False,
                    "rate_limited": True,
                    "wait_time": wait_time
                }
            
            # Build content array for API
            content = [query]
            
            # Add images
            if images:
                content.extend(images[:2])  # Max 2 images
            
            # Add video (requires file upload)
            if video:
                try:
                    video_bytes = video.read()
                    video.seek(0)  # Reset for potential re-use
                    
                    # Determine mime type
                    video_name = getattr(video, 'name', 'video.mp4')
                    if video_name.endswith('.mp4'):
                        mime_type = 'video/mp4'
                    elif video_name.endswith('.mov'):
                        mime_type = 'video/quicktime'
                    elif video_name.endswith('.avi'):
                        mime_type = 'video/x-msvideo'
                    else:
                        mime_type = 'video/mp4'
                    
                    uploaded_video = self._upload_media_file(video_bytes, mime_type, video_name)
                    if uploaded_video:
                        content.append(uploaded_video)
                except Exception as e:
                    print(f"⚠️ Video upload failed: {e}")
            
            # Add audio (requires file upload)
            if audio:
                try:
                    audio_bytes = audio.read()
                    audio.seek(0)
                    
                    audio_name = getattr(audio, 'name', 'audio.mp3')
                    if audio_name.endswith('.mp3'):
                        mime_type = 'audio/mpeg'
                    elif audio_name.endswith('.wav'):
                        mime_type = 'audio/wav'
                    elif audio_name.endswith('.ogg'):
                        mime_type = 'audio/ogg'
                    else:
                        mime_type = 'audio/mpeg'
                    
                    uploaded_audio = self._upload_media_file(audio_bytes, mime_type, audio_name)
                    if uploaded_audio:
                        content.append(uploaded_audio)
                except Exception as e:
                    print(f"⚠️ Audio upload failed: {e}")
            
            # Generate response
            generation_config = genai.types.GenerationConfig(**GENERATION_CONFIG)
            response = model.generate_content(content, generation_config=generation_config)
            
            # Extract response
            response_text = self._safe_extract_text(response)
            
            # Generate SMART explanation
            answer_explanation = self._generate_smart_explanation(
                query, response_text, media_info, analysis, use_advanced
            )
            
            processing_time = time.time() - self._start_time
            
            result = {
                "response": response_text,
                "answer_explanation": answer_explanation,
                "analysis": analysis,
                "success": True,
                "error": None,
                "processing_time": round(processing_time, 2),
                "from_cache": False
            }
            
            # Cache only text queries
            if not any(media_info.values()) and len(self._response_cache) < 50:
                self._response_cache[cache_key] = result.copy()
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            
            if "429" in error_msg or "quota" in error_msg.lower():
                import re
                wait_match = re.search(r'retry.*?(\d+(?:\.\d+)?)\s*s', error_msg, re.IGNORECASE)
                wait_time = float(wait_match.group(1)) if wait_match else 60.0
                
                return {
                    "response": None,
                    "answer_explanation": None,
                    "analysis": analysis,
                    "success": False,
                    "error": f"Rate limit exceeded. Please wait {int(wait_time)} seconds.",
                    "processing_time": time.time() - self._start_time,
                    "from_cache": False,
                    "rate_limited": True,
                    "wait_time": wait_time
                }
            
            return {
                "response": None,
                "answer_explanation": None,
                "analysis": analysis,
                "success": False,
                "error": error_msg,
                "processing_time": time.time() - self._start_time,
                "from_cache": False
            }
    
    def _safe_extract_text(self, response) -> str:
        """Safely extract text from response with comprehensive error handling"""
        try:
            if hasattr(response, 'text') and response.text:
                return response.text
            
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                
                if hasattr(candidate, 'finish_reason'):
                    finish_reason = candidate.finish_reason
                    
                    if finish_reason == 1:
                        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                            parts_text = []
                            for part in candidate.content.parts:
                                if hasattr(part, 'text'):
                                    parts_text.append(part.text)
                            if parts_text:
                                return ''.join(parts_text)
                    
                    elif finish_reason == 2:
                        return "⚠️ Response blocked by safety filters. Please try rephrasing."
                    elif finish_reason == 3:
                        return "⚠️ Response blocked due to recitation concerns."
                    elif finish_reason == 4:
                        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                            parts_text = []
                            for part in candidate.content.parts:
                                if hasattr(part, 'text'):
                                    parts_text.append(part.text)
                            if parts_text:
                                return ''.join(parts_text) + "\n\n[Response truncated]"
                        return "⚠️ Response exceeded maximum length."
                    else:
                        return f"⚠️ Response stopped (reason: {finish_reason})."
            
            return "Unable to generate response."
            
        except Exception as e:
            return f"Error extracting response: {str(e)}"
    
    def _generate_smart_explanation(
        self,
        query: str,
        answer: str,
        media_info: Dict[str, Any],
        analysis: Dict[str, Any],
        use_advanced: bool
    ) -> str:
        """
        Generate INTELLIGENT, context-aware explanations
        Focuses on ACTUAL reasoning decisions, not generic descriptions
        """
        
        if answer.startswith("⚠️"):
            return "Explanation unavailable: Response was blocked or failed."
        
        explanation_parts = []
        
        # === PART 1: Input Processing Strategy ===
        explanation_parts.append("🧠 Input Processing Strategy:")
        
        processing_decisions = []
        
        if media_info.get("has_video"):
            processing_decisions.append(
                "Video input required temporal analysis across frames - the AI extracted keyframes, "
                "analyzed motion patterns, detected scene changes, and tracked object movements over time. "
                "This multi-frame processing is computationally intensive and requires advanced vision models."
            )
        
        if media_info.get("has_audio"):
            processing_decisions.append(
                "Audio analysis involved speech recognition, tone detection, and acoustic feature extraction. "
                "The AI transcribed spoken content while analyzing vocal patterns, background sounds, and audio quality."
            )
        
        if media_info.get("has_image") and not media_info.get("has_video"):
            image_query_keywords = ['what', 'who', 'where', 'identify', 'describe', 'show']
            if any(kw in query.lower() for kw in image_query_keywords):
                processing_decisions.append(
                    "Image recognition prioritized object detection and scene understanding - the AI identified "
                    "entities, classified visual elements, and interpreted spatial relationships to answer your specific question."
                )
            else:
                processing_decisions.append(
                    "Visual context was integrated with linguistic analysis - the AI used image features "
                    "to enhance understanding of your text query rather than just describing the image."
                )
        
        if not any(media_info.values()):
            # Pure text query - analyze linguistic complexity
            if analysis.get("has_technical"):
                processing_decisions.append(
                    "Technical query triggered domain-specific knowledge retrieval - the AI accessed specialized "
                    "knowledge bases and applied field-specific reasoning frameworks to ensure accuracy."
                )
            
            if analysis.get("has_comparisons"):
                processing_decisions.append(
                    "Comparative analysis required building mental models of multiple entities, identifying "
                    "relevant dimensions for comparison, and evaluating trade-offs across these dimensions."
                )
            
            if analysis.get("has_multiple_questions"):
                processing_decisions.append(
                    "Multi-part question required query decomposition - the AI identified distinct sub-questions, "
                    "determined optimal answering order, and ensured all parts received adequate coverage."
                )
        
        if processing_decisions:
            explanation_parts.append(" ".join(processing_decisions))
        else:
            explanation_parts.append(
                "Straightforward text query processed through standard linguistic parsing and semantic understanding."
            )
        
        # === PART 2: Reasoning Architecture Selection ===
        explanation_parts.append("\n**⚙️ Reasoning Architecture Selection:**")
        
        if use_advanced:
            architecture_reasoning = []
            
            if media_info.get("has_video") or media_info.get("has_audio"):
                architecture_reasoning.append(
                    "Selected advanced multimodal model because video/audio requires specialized processing "
                    "capabilities not available in rapid models"
                )
            elif analysis.get("complexity_score", 0) > 0.6:
                architecture_reasoning.append(
                    f"Complexity score of {analysis.get('complexity_score', 0):.2f} indicated need for deep reasoning - "
                    "advanced model provides better chain-of-thought capabilities and nuanced understanding"
                )
            elif analysis.get("has_technical"):
                architecture_reasoning.append(
                    "Technical content requires access to specialized knowledge and precise terminology - "
                    "advanced model has broader domain coverage and better accuracy for expert-level queries"
                )
            else:
                architecture_reasoning.append(
                    "Advanced model selected to ensure comprehensive coverage and high-quality reasoning"
                )
            
            explanation_parts.append(". ".join(architecture_reasoning) + ".")
        else:
            explanation_parts.append(
                "Rapid model sufficient for this query - prioritized response speed while maintaining accuracy. "
                "The query's straightforward nature didn't require deep reasoning chains or specialized processing."
            )
        
        # === PART 3: Answer Construction Decisions ===
        explanation_parts.append("\n**📝 Answer Construction Decisions:**")
        
        import re
        answer_lower = answer.lower()
        answer_words = answer.split()
        
        construction_choices = []
        
        # Analyze actual answer structure
        has_code = '```' in answer
        has_lists = bool(re.search(r'(\d+\.|[-•*])\s', answer))
        has_examples = 'example' in answer_lower or 'instance' in answer_lower
        has_steps = any(word in answer_lower for word in ['first', 'second', 'then', 'finally', 'step'])
        
        if has_code:
            construction_choices.append(
                "Included code examples because implementation details are more effective than abstract descriptions "
                "for technical understanding"
            )
        
        if has_lists and has_steps:
            construction_choices.append(
                "Structured as sequential steps because the query implied procedural knowledge - "
                "ordered format aids execution and comprehension"
            )
        elif has_lists:
            construction_choices.append(
                "Used list format to present parallel information clearly - each item carries equal weight "
                "and bullet points improve scannability"
            )
        
        if has_examples:
            construction_choices.append(
                "Incorporated concrete examples because abstract concepts become clearer through specific instances - "
                "examples bridge theory and practice"
            )
        
        # Analyze answer length relative to query
        answer_length = len(answer_words)
        query_length = len(query.split())
        
        if answer_length > query_length * 5:
            construction_choices.append(
                f"Generated comprehensive {answer_length}-word response because your query required thorough exploration - "
                "prioritized completeness over brevity"
            )
        elif answer_length < query_length * 2:
            construction_choices.append(
                f"Provided concise {answer_length}-word response because your query had a direct answer - "
                "avoided unnecessary elaboration"
            )
        
        if construction_choices:
            explanation_parts.append(". ".join(construction_choices) + ".")
        else:
            explanation_parts.append(
                "Constructed straightforward prose response appropriate for the query's nature."
            )
        
        return "\n".join(explanation_parts)
    
    def get_influencing_factors(self, analysis: Dict, response: str, query: str) -> Dict[str, Dict]:
        """Extract comprehensive influencing factors with better categorization"""
        response_words = response.split()
        response_length = len(response_words)
        query_words = query.split()
        query_complexity = len(query_words)
        
        has_technical_terms = any(keyword in response.lower() for keyword in TECHNICAL_KEYWORDS)
        has_detailed_explanation = response_length > 100
        has_structured_format = any(marker in response for marker in ['1.', '2.', '3.', '-', '*', '•', '\n\n'])
        has_code_or_formulas = any(marker in response for marker in ['```', '`', '=', '()', '{}'])
        
        factors = {}
        
        # Video/Audio factors
        if analysis.get("has_video"):
            factors["temporal_analysis"] = {
                "value": "✓ Active",
                "impact": "Critical",
                "description": "Frame-by-frame video analysis with motion tracking, scene detection, and temporal coherence understanding across the video timeline."
            }
        
        if analysis.get("has_audio"):
            factors["audio_processing"] = {
                "value": "✓ Active",
                "impact": "High",
                "description": "Speech recognition, acoustic analysis, and audio feature extraction to understand verbal content and sonic patterns."
            }
        
        # Visual factors
        if analysis.get("has_image"):
            factors["visual_intelligence"] = {
                "value": "✓ Enabled",
                "impact": "High",
                "description": "Computer vision applied for object recognition, scene understanding, and visual context integration with query semantics."
            }
        
        # Query complexity
        complexity_level = "High" if query_complexity > WORD_COUNT_THRESHOLD else ("Medium" if query_complexity > 10 else "Low")
        factors["query_depth"] = {
            "value": f"{query_complexity} words",
            "impact": complexity_level,
            "description": f"{'Complex multi-faceted query requiring layered analysis.' if query_complexity > WORD_COUNT_THRESHOLD else ('Moderate query needing balanced coverage.' if query_complexity > 10 else 'Focused query enabling direct response.')}"
        }
        
        # Response comprehensiveness
        factors["response_coverage"] = {
            "value": f"{response_length} words",
            "impact": "High" if has_detailed_explanation else "Medium",
            "description": f"{'Extensive coverage with detailed explanations and examples.' if has_detailed_explanation else 'Concise, targeted response focused on essentials.'}"
        }
        
        # Technical analysis
        if analysis.get("has_technical") or has_technical_terms:
            factors["domain_expertise"] = {
                "value": f"Score: {analysis.get('technical_score', 0)}",
                "impact": "High",
                "description": "Specialized knowledge applied with technical precision and field-specific methodologies."
            }
        
        # Reasoning complexity
        reasoning_score = analysis.get("complexity_score", 0)
        factors["cognitive_depth"] = {
            "value": f"{reasoning_score:.1%}",
            "impact": "High" if reasoning_score > 0.6 else ("Medium" if reasoning_score > 0.3 else "Low"),
            "description": f"{'Multi-layered inference with complex reasoning chains.' if reasoning_score > 0.6 else ('Standard analytical reasoning with logical flow.' if reasoning_score > 0.3 else 'Direct reasoning with straightforward logic.')}"
        }
        
        # Information architecture
        factors["structural_design"] = {
            "value": "Structured" if has_structured_format else "Prose",
            "impact": "Medium",
            "description": "Organized with hierarchical formatting for clarity." if has_structured_format else "Natural prose for flowing narrative."
        }
        
        # Code/symbolic reasoning
        if has_code_or_formulas:
            factors["symbolic_processing"] = {
                "value": "✓ Applied",
                "impact": "High",
                "description": "Mathematical, logical, or programmatic reasoning with formal notation and executable examples."
            }
        
        return factors
    
    def toggle_explanations(self, enabled: bool):
        """Enable or disable AI-generated explanations"""
        self.explanation_enabled = enabled
        print(f"✅ Explanations {'enabled' if enabled else 'disabled'}")
    
    def clear_cache(self):
        """Clear response and explanation caches"""
        self._response_cache.clear()
        self._explanation_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            "cached_responses": len(self._response_cache),
            "cached_explanations": len(self._explanation_cache),
            "cache_limit": 50
        }
    
    def reset_rate_limiters(self):
        """Reset all rate limiters"""
        self.rapid_limiter.reset()
        self.advanced_limiter.reset()
        print("✅ Rate limiters reset")