; Svelte component references in templates
; HTML standard tags won't match definitions elsewhere, so harmless noise

(start_tag
  (tag_name) @name.reference.component) @reference.component

(self_closing_tag
  (tag_name) @name.reference.component) @reference.component
